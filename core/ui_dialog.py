import os
import sys
import shutil
import subprocess

def show_modern_adwaita_dialog(file_info: dict, options: list, filename: str):
    """
    Shows a modern, spacious GNOME Libadwaita / GTK4 dialog with large text and buttons.
    Returns:
      (True, chosen_option) -> User selected an option and clicked Convert
      (True, None)          -> User clicked Cancel or closed the window
      (False, None)         -> Framework failed / Exception, need fallback
    """
    try:
        import gi
        gi.require_version('Gtk', '4.0')
        gi.require_version('Adw', '1')
        from gi.repository import Gtk, Adw, Gio

        selected_result = {"choice": options[0] if options else None, "confirmed": False}

        class AutoConvertApp(Adw.Application):
            def __init__(self):
                app_id = f"com.filetofile.autoconvert.p{os.getpid()}"
                super().__init__(application_id=app_id, flags=Gio.ApplicationFlags.FLAGS_NONE)

            def do_activate(self):
                win = Adw.ApplicationWindow(application=self)
                win.set_title("⚡ Smart Auto Convert")
                win.set_default_size(740, 600)
                win.set_modal(True)

                # Main vertical container
                main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
                main_box.set_margin_top(24)
                main_box.set_margin_bottom(24)
                main_box.set_margin_start(28)
                main_box.set_margin_end(28)

                # 1. Header / File Info Group
                info_group = Adw.PreferencesGroup()
                info_group.set_title("รายละเอียดไฟล์ที่เลือก")
                info_group.set_description(f"🔍 ตรวจพบ: <b>{file_info.get('desc', 'Unknown')}</b>")

                file_row = Adw.ActionRow()
                file_row.set_title(f"<span size='large' weight='bold'>{filename}</span>")
                file_row.set_subtitle(f"MIME Type: {file_info.get('mime', 'N/A')}")
                file_row.set_icon_name("document-properties-symbolic")
                info_group.add(file_row)
                main_box.append(info_group)

                # 2. Target Format Options Group
                opt_group = Adw.PreferencesGroup()
                opt_group.set_title("เลือกรูปแบบที่ต้องการแปลง (Target Format)")
                opt_group.set_description("คลิกเลือกฟอร์แมตผลลัพธ์ที่ต้องการ:")

                first_check = None

                for i, opt in enumerate(options):
                    key, title, module, action = opt
                    row = Adw.ActionRow()
                    row.set_title(f"<span size='medium' weight='bold'>ฟอร์แมต: {key.upper()}</span>")
                    row.set_subtitle(f"<span size='medium'>{title}</span>")

                    check = Gtk.CheckButton()
                    if first_check is None:
                        first_check = check
                        check.set_active(True)
                        selected_result["choice"] = opt
                    else:
                        check.set_group(first_check)

                    def make_toggled(current_opt):
                        def on_toggled(btn):
                            if btn.get_active():
                                selected_result["choice"] = current_opt
                        return on_toggled

                    check.connect("toggled", make_toggled(opt))
                    row.add_prefix(check)
                    row.set_activatable_widget(check)
                    opt_group.add(row)

                # Scrolled window in case of many options
                scroll = Gtk.ScrolledWindow()
                scroll.set_vexpand(True)
                scroll.set_child(opt_group)
                main_box.append(scroll)

                # 3. Bottom Action Buttons
                btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
                btn_box.set_halign(Gtk.Align.END)
                btn_box.set_margin_top(8)

                cancel_btn = Gtk.Button(label="ยกเลิก")
                cancel_btn.add_css_class("flat")
                cancel_btn.set_size_request(110, 48)

                def on_cancel(btn):
                    selected_result["confirmed"] = False
                    win.close()
                    self.quit()

                cancel_btn.connect("clicked", on_cancel)
                btn_box.append(cancel_btn)

                convert_btn = Gtk.Button(label="🚀 เริ่มแปลงไฟล์ทันที")
                convert_btn.add_css_class("suggested-action")
                convert_btn.add_css_class("pill")
                convert_btn.set_size_request(200, 48)

                def on_convert(btn):
                    selected_result["confirmed"] = True
                    win.close()
                    self.quit()

                convert_btn.connect("clicked", on_convert)
                btn_box.append(convert_btn)

                main_box.append(btn_box)

                win.set_content(main_box)
                win.present()

        app = AutoConvertApp()
        app.run([])

        if selected_result["confirmed"]:
            return (True, selected_result["choice"])
        else:
            return (True, None)  # User closed/canceled window deliberately

    except Exception as e:
        # Framework failed, fall back
        return (False, None)

def show_fallback_zenity_dialog(file_info: dict, options: list, filename: str):
    """
    Enlarged, spacious Zenity dialog as reliable fallback.
    """
    if not shutil.which("zenity") or not os.environ.get("DISPLAY"):
        return options[0] if options else None

    cmd = [
        "zenity", "--list", "--radiolist",
        "--title=⚡ Smart Auto Convert",
        f"--text=\n<b><big><big>ตรวจพบ: {file_info['desc']}</big></big></b>\nไฟล์: <i><big>{filename}</big></i>\n\n<b>กรุณาเลือกรูปแบบที่ต้องการแปลง:</b>\n",
        "--column=เลือก", "--column=รหัส", "--column=รูปแบบผลลัพธ์",
        "--height=580", "--width=800"
    ]

    for i, (key, desc, _, _) in enumerate(options):
        selected = "TRUE" if i == 0 else "FALSE"
        cmd.extend([selected, key.upper(), desc])

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        chosen_key = res.stdout.strip().lower()
        if not chosen_key:
            return None  # Canceled
        for opt in options:
            if opt[0].lower() == chosen_key:
                return opt
    except Exception:
        pass

    return options[0] if options else None

def select_target_format(file_info: dict, options: list, filename: str):
    """
    Displays the UI dialog: prefers modern Libadwaita/GTK4, falls back to enlarged Zenity.
    """
    handled, choice = show_modern_adwaita_dialog(file_info, options, filename)
    if handled:
        return choice

    # If Adwaita was unavailable, use enlarged Zenity
    return show_fallback_zenity_dialog(file_info, options, filename)

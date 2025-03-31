import os
import shutil
import ctypes
import subprocess
import winreg
import psutil
import time

STEALTH_NAMES = [
    "WinSxSHost.exe", "svchst.exe", "explorre.exe", "OneDr1veSync.exe", "sysdiaghoster.exe",
    "MsMpEgine32.exe", "taskhostw64.exe", "conhost2.exe", "spoold32.exe", "defupdate32.exe",
    "cortnanaHelper.exe", "RuntimeSysHost.exe", "update_module.exe", "edge_loader.exe",
    "netcfgsvc.exe", "usbchost.exe", "WinAudioHlp.exe", "svch0stHlp.exe", "systemnt.exe",
    "autoupdtr.exe", "dllcachehost.exe", "WinSyncTray.exe", "ShellSysTask.exe", "winhlper.exe",
    "driverchk.exe", "CrashHandlerSrv.exe", "audiofxhost.exe", "dwmexec32.exe", "WinIdleTask.exe",
    "msdnsconfig.exe", "netsh_helper.exe", "bootrecsvc.exe", "cloudprovider64.exe", "ntdlldrhost.exe",
    "msdbupdater.exe", "printvwrhost.exe", "diskhost64.exe", "LogiSrvSync.exe", "WpnUserServicex.exe",
    "edgebgsvc.exe", "usbhid32svc.exe", "MouseSrvHost.exe", "kbdntask32.exe", "netbioshlp.exe",
    "fontcachex.exe", "DbgHelpSvc.exe", "audioCpl32.exe", "hostsyscore.exe", "AppXloader.exe",
    "lsasscopy.exe", "ntqueryhost.exe", "smartscreen64x.exe", "backgroundedgetray.exe",
    "SecureBootSync.exe", "AudioDumpSys.exe", "rdpcfgmanager.exe", "oobeservice64.exe",
    "MsSrvContainer.exe", "taskmanui.exe", "ProcessIdle32.exe", "windbglaunch.exe", "powershellpx.exe",
    "svch0std.exe", "SecureSettingsLoader.exe", "cmdbackdrop.exe", "WuaUsrHost.exe",
    "usbconfigurator.exe", "wificonfigsx.exe", "MsSpoolInit.exe", "dnsupdaterhelper.exe",
    "FirewallNetHost.exe", "bootoptmgr.exe", "ShellHostX64.exe", "certlmupdate.exe",
    "SystemIdleSrv.exe", "nethosthelper.exe", "WinBootProc.exe", "regsvcchk.exe", "winloginplus.exe",
    "bootentrytool.exe", "vmhostsvc.exe", "hypervloader.exe", "syspolicymgr.exe", "hostinfocore.exe",
    "dxgkrnlproxy.exe", "graphupdatehost.exe", "keybdloader.exe", "taskmanx32.exe", "usbmountsvc.exe",
    "nvctrlhost.exe", "speechtasker.exe", "HidSrvHost.exe", "cryptobackup.exe", "msloadcheck.exe",
    "wlanhosttask.exe", "keyboardidle.exe", "accessibilityhost.exe", "driverhost64.exe",
    "hvcpphost.exe", "protectioninit.exe"
]

APPDATA_PATH = os.getenv("APPDATA") + "\\Microsoft\\Windows\\"

def kill_running_instances():
    print("[*] Looking for Running Instances...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] in STEALTH_NAMES:
                print(f"[!] Ending Proccess: {proc.info['name']}")
                proc.kill()
        except Exception as e:
            print(e)
            continue

def delete_files():
    print("[*] Controlling APPDATA...")
    for name in STEALTH_NAMES:
        path = os.path.join(APPDATA_PATH, name)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"[+] Removed: {path}")
            except Exception as e:
                print(f"[!] Couldn't remove: {path} ({e})")

def delete_registry_persistence():
    print("[*] Controlling Registry Entries...")
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
            for name in STEALTH_NAMES:
                try:
                    winreg.DeleteValue(key, name)
                    print(f"[+] Registry'den silindi: {name}")
                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"[!] Registry Clean Error: {e}")
    except Exception as e:
        print(f"[!] Couldn't acces to registry: {e}")

def delete_scheduled_tasks():
    print("[*] Controlling Scheduled Tasks...")
    for name in STEALTH_NAMES:
        try:
            subprocess.run(["schtasks", "/delete", "/tn", name, "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            continue

def main():
    print("[*] Cleaning Proccess starting...")
    kill_running_instances()
    time.sleep(1)
    delete_files()
    delete_registry_persistence()
    delete_scheduled_tasks()
    print("[✔] Cleaning completed.")

if __name__ == "__main__":
    main()
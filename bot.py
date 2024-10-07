
import requests,time,json,sys
from datetime import datetime
from colorama import Fore, Style, init

# Inisialisasi Colorama
init(autoreset=True)

def get_current_time():
    return datetime.now().strftime("[%d/%m/%Y %H:%M]")

def ll(js):
    print(json.dumps(js, indent=4))

def daly_bonus(token):
    url = "https://api.miniapp.dropstab.com/api/bonus/dailyBonus"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if(response.status_code==401):
        print(f'{Fore.RED}TOKEN_EXPIRED_OR_INVALID ...!')
        exit()
    daily=response.json()
    if(daily['result']==True):
        print(f"{Fore.WHITE} { get_current_time()}  {Fore.YELLOW}Daily Bonus  - Streaks:{daily['streaks']}  {Fore.GREEN} Bonus:{daily['bonus']} {Style.RESET_ALL}")

def compilte_verify(token):
    url = f"https://api.miniapp.dropstab.com/api/quest/completed"
    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def verify_task(task_id,token):
    url = f"https://api.miniapp.dropstab.com/api/quest/{task_id}/verify"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.request("PUT", url, headers=headers, data=payload)

def get_task(token):
    url = "https://api.miniapp.dropstab.com/api/quest/active"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def output_task(tasks,token):
    # print(json.dumps(tasks, indent=4))
    for i,group in enumerate(tasks):
        for task in group['quests']:
            # ll(task)
            if(task['claimAllowed']==False):
                if(task['status']=="VERIFICATION"):
                    warna=Fore.YELLOW
                    print(f"{Fore.WHITE} { get_current_time()}  {group['name']} - {task['name']}{Style.RESET_ALL} : {warna} {task['status']} {Style.RESET_ALL}")
                else:
                    task_verify=verify_task(task['id'],token)
                    if task_verify.status_code==200 and task_verify.json()['status']=="OK":
                        warna=Fore.YELLOW
                        print(f"{Fore.WHITE} { get_current_time()}  {group['name']} - {task['name']}{Style.RESET_ALL} : {warna} {task['status']} {Style.RESET_ALL}")
                    else:
                        warna=Fore.RED
                        print(f"{Fore.WHITE} { get_current_time()}  {group['name']} - {task['name']}{Style.RESET_ALL} : {warna} {task['status']} {Style.RESET_ALL}")
            else:
                claim=claim_task(task['id'],token)
                if(claim.status_code==200):
                    print(f"{Fore.WHITE} { get_current_time()}  {group['name']} - {task['name']}{Style.RESET_ALL} : {Fore.GREEN} OK {Style.RESET_ALL}")

def get_user(token):
    # compilte_verify(token)
    url = "https://api.miniapp.dropstab.com/api/user/current"
    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def claim_task(quest_id,token):
    url = f"https://api.miniapp.dropstab.com/api/quest/{quest_id}/claim"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("PUT", url, headers=headers)
    return response

def get_token():
    tokens = []
    try:
        # Membaca file token.txt
        with open('token.txt', 'r') as file:
            tokens = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("File token.txt tidak ditemukan.")
    
    return tokens

def output_user(index,user):
    print('=======================================================================')
    print(f"{Fore.WHITE} { get_current_time()}  Account Ke-{index+1} {Fore.YELLOW}{user['tgUsername']}{Style.RESET_ALL}  | Balance  {Fore.GREEN}{user['balance']}{Style.RESET_ALL}")
def countdown(hours):
    total_seconds = hours * 3600  # Menghitung total detik dari jam
    for remaining in range(total_seconds, 0, -1):
        # Menghitung jam, menit, dan detik tersisa
        hrs, mins, secs = remaining // 3600, (remaining % 3600) // 60, remaining % 60
        # Format string waktu
        timer = f"{hrs:02}:{mins:02}:{secs:02}"
        
        # Menampilkan timer tanpa berpindah baris
        sys.stdout.write('\r' + timer)  # Menggunakan '\r' untuk kembali ke awal baris
        sys.stdout.flush()  # Memastikan output ditampilkan
        time.sleep(1)  # Tunggu 1 detik

    print("\nCountdown selesai!")

def main():
    try:
        while True:
            tokens = get_token()  # Memanggil fungsi get_token untuk mengambil daftar token

            for i,token in enumerate(tokens):
                
                daly_bonus(token)
                user=get_user(token)
                output_user(i,user)
                tasks=get_task(token)
                output_task(tasks,token)
            countdown(1)
    except KeyboardInterrupt:
        print("\nBot By AF09")

# Menjalankan program utama
if __name__ == "__main__":
    main()
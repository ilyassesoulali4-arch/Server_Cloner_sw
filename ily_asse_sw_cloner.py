import sys
import json
import os
import time
import asyncio
import base64
import requests

APP_NAME = "ily_asse_sw_cloner"
DEV_NAME = "ilyasse_dev"
VERSION = "3.0.0"

BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

C = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "reset": "\033[0m",
    "cls": "\033[2J\033[H"
}

def cprint(text, color="white", bold=False):
    c = C.get(color, C["white"])
    b = C["bold"] if bold else ""
    print(f"{b}{c}{text}{C['reset']}")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    clear()
    sys.stdout.reconfigure(encoding='utf-8')
    banner = f"""
{C['cyan']}{C['bold']}  +=========================================+
  |       {C['magenta']}ILYASSE SW CLONER{C['cyan']} v{VERSION}         |
  |           {C['yellow']}by {DEV_NAME}{C['cyan']}                |
  +=========================================+{C['reset']}

{C['dim']}  >> Professional Discord Server Cloner <<{C['reset']}
{C['green']}  -----------------------------------------{C['reset']}
    """
    print(banner)

def show_menu():
    print(f"\n{C['bold']}{C['white']}  [1]{C['reset']} {C['cyan']}Clone Server{C['reset']}")
    print(f"  {C['bold']}{C['white']}[2]{C['reset']} {C['cyan']}Set Token{C['reset']}")
    print(f"  {C['bold']}{C['white']}[3]{C['reset']} {C['cyan']}Show Token Info{C['reset']}")
    print(f"  {C['bold']}{C['white']}[4]{C['reset']} {C['cyan']}Clone to Existing Server{C['reset']}")
    print(f"  {C['bold']}{C['white']}[5]{C['reset']} {C['cyan']}Help / Info{C['reset']}")
    print(f"  {C['bold']}{C['white']}[6]{C['reset']} {C['red']}Exit{C['reset']}")
    print(f"\n{C['green']}  -----------------------------------------{C['reset']}")

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token, "saved_at": time.strftime("%Y-%m-%d %H:%M:%S")}, f)
    cprint("  [OK] Token saved successfully!", "green", True)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            data = json.load(f)
            return data.get("token")
    return None

def get_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

def fetch_guilds(token):
    r = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def fetch_guild_channels(token, guild_id):
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def fetch_guild_roles(token, guild_id):
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def fetch_guild_emojis(token, guild_id):
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/emojis", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def fetch_guild_stickers(token, guild_id):
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/stickers", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def fetch_guild_widget(token, guild_id):
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/widget", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def fetch_guild(token, guild_id):
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def fetch_me(token):
    r = requests.get("https://discord.com/api/v10/users/@me", headers=get_headers(token))
    if r.status_code == 200:
        return r.json()
    return None

def create_guild(token, name):
    payload = {
        "name": name[:100],
        "channels": [{"name": "general", "type": 0}]
    }
    for attempt in range(3):
        r = requests.post("https://discord.com/api/v10/guilds", headers=get_headers(token), json=payload)
        if r.status_code == 429:
            retry_after = float(r.headers.get("Retry-After", "5") or 5)
            cprint(f"  [429] Rate limited... retrying in {int(retry_after)}s ({attempt + 1}/3)", "yellow")
            time.sleep(min(retry_after, 60))
            continue
        if r.status_code in (200, 201):
            return r.json(), r
        return None, r
    return None, r

def create_guild_channel(token, guild_id, data):
    r = requests.post(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=get_headers(token), json=data)
    return r.status_code in (200, 201)

def create_guild_role(token, guild_id, data):
    r = requests.post(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=get_headers(token), json=data)
    if r.status_code in (200, 201):
        return r.json()
    return None

def create_guild_emoji(token, guild_id, name, image_b64):
    r = requests.post(f"https://discord.com/api/v10/guilds/{guild_id}/emojis", headers=get_headers(token), json={
        "name": name,
        "image": image_b64
    })
    return r.status_code in (200, 201)

def set_guild_settings(token, guild_id, settings):
    r = requests.patch(f"https://discord.com/api/v10/guilds/{guild_id}", headers=get_headers(token), json=settings)
    return r.status_code == 200

def delete_guild(token, guild_id):
    r = requests.delete(f"https://discord.com/api/v10/guilds/{guild_id}", headers=get_headers(token))
    return r.status_code == 204

def progress_bar(current, total, bar_length=30, prefix="", suffix=""):
    if total == 0:
        return
    filled = int(bar_length * current // total)
    bar = "#" * filled + "." * (bar_length - filled)
    pct = f"{current}/{total}"
    sys.stdout.write(f"\r  {prefix} [{C['green']}{bar}{C['reset']}] {C['yellow']}{pct}{C['reset']} {suffix}")
    sys.stdout.flush()

async def clone_to_existing(token, source_id, target_id):
    show_banner()
    cprint("  [*] Initializing clone to existing server...", "cyan", True)

    source = fetch_guild(token, source_id)
    target_check = fetch_guild(token, target_id)
    if not source:
        cprint("  [X] Failed to fetch source server! Check the ID.", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return
    if not target_check:
        cprint("  [X] Failed to fetch target server! Check the ID.", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    cprint(f"\n  [Source] {source['name']} ({source_id})", "green")
    cprint(f"  [Target] {target_check['name']} ({target_id})", "cyan")
    cprint(f"\n  {C['red']}{C['bold']}  [!] WARNING: This will DELETE all existing channels & roles in target! Continue? (y/n){C['reset']}")
    confirm = input(f"  {C['cyan']}> {C['reset']}").strip().lower()
    if confirm != "y":
        cprint("  [!] Cancelled.", "yellow")
        return

    existing_channels = fetch_guild_channels(token, target_id) or []
    cprint(f"\n  {C['yellow']}[*] Cleaning target server ({len(existing_channels)} channels)...{C['reset']}")
    for ch in existing_channels:
        r = requests.delete(f"https://discord.com/api/v10/channels/{ch['id']}", headers=get_headers(token))
        if r.status_code in (200, 204):
            cprint(f"    Deleted: #{ch['name']}", "dim")
        time.sleep(0.3)

    existing_roles = fetch_guild_roles(token, target_id) or []
    for role in existing_roles:
        if role["name"] == "@everyone":
            continue
        r = requests.delete(f"https://discord.com/api/v10/guilds/{target_id}/roles/{role['id']}", headers=get_headers(token))
        if r.status_code in (200, 204):
            cprint(f"    Deleted role: {role['name']}", "dim")
        time.sleep(0.3)

    await clone_worker(token, source_id, target_id, source, target_check['name'])

async def clone_worker(token, source_id, target_id, source, target_name=None):
    channels = fetch_guild_channels(token, source_id) or []
    roles = fetch_guild_roles(token, source_id) or []
    emojis = fetch_guild_emojis(token, source_id) or []
    stickers = fetch_guild_stickers(token, source_id) or []

    channels.sort(key=lambda c: c.get("position", 0))
    roles.sort(key=lambda r: r.get("position", 0), reverse=True)

    cprint(f"\n  {C['yellow']}[*] Cloning Roles ({len(roles)})...{C['reset']}")
    role_map = {}
    for i, role in enumerate(roles):
        if role["name"] == "@everyone":
            role_map[role["id"]] = target_id
            continue
        perms = int(role.get("permissions", "0"))
        role_data = {
            "name": role["name"],
            "permissions": str(perms),
            "color": role.get("color", 0),
            "hoist": role.get("hoist", False),
            "mentionable": role.get("mentionable", False),
        }
        new_role = create_guild_role(token, target_id, role_data)
        if new_role:
            role_map[role["id"]] = new_role["id"]
        progress_bar(i + 1, len(roles), prefix="Roles", suffix=f"{role['name']}")
    print()

    cprint(f"\n  {C['yellow']}[*] Cloning Channels ({len(channels)})...{C['reset']}")
    cat_channels = [c for c in channels if c["type"] == 4]
    text_channels = [c for c in channels if c["type"] == 0]
    voice_channels = [c for c in channels if c["type"] == 2]
    forum_channels = [c for c in channels if c["type"] in (5, 13, 15)]

    cat_map = {}
    for i, cat in enumerate(cat_channels):
        perms = []
        for overwrite in cat.get("permission_overwrites", []):
            perms.append({
                "id": role_map.get(overwrite["id"], overwrite["id"]),
                "type": overwrite["type"],
                "allow": overwrite.get("allow", "0"),
                "deny": overwrite.get("deny", "0"),
            })
        data = {
            "name": cat["name"],
            "type": 4,
            "position": cat.get("position", 0),
            "permission_overwrites": perms,
        }
        if create_guild_channel(token, target_id, data):
            cat_map[cat["id"]] = True
        progress_bar(i + 1, len(cat_channels), prefix="Categories", suffix=f"{cat['name']}")
    print()

    new_channels = fetch_guild_channels(token, target_id) or []
    new_cats = {c["name"]: c["id"] for c in new_channels if c["type"] == 4}

    all_other = sorted(
        [c for c in channels if c["type"] in (0, 2, 5, 13, 15)],
        key=lambda c: c.get("position", 0)
    )
    for i, ch in enumerate(all_other):
        perms = []
        for overwrite in ch.get("permission_overwrites", []):
            perms.append({
                "id": role_map.get(overwrite["id"], overwrite["id"]),
                "type": overwrite["type"],
                "allow": overwrite.get("allow", "0"),
                "deny": overwrite.get("deny", "0"),
            })
        parent_name = None
        if ch.get("parent_id") and ch["parent_id"] in cat_map:
            for cat in cat_channels:
                if cat["id"] == ch["parent_id"]:
                    parent_name = cat["name"]
                    break
        data = {
            "name": ch["name"],
            "type": ch["type"],
            "position": ch.get("position", 0),
            "permission_overwrites": perms,
            "topic": ch.get("topic", ""),
            "nsfw": ch.get("nsfw", False),
            "bitrate": ch.get("bitrate", 64000),
            "user_limit": ch.get("user_limit", 0),
        }
        if parent_name and parent_name in new_cats:
            data["parent_id"] = new_cats[parent_name]
        if ch["type"] == 0:
            data.pop("bitrate", None)
            data.pop("user_limit", None)
        else:
            data.pop("topic", None)
        create_guild_channel(token, target_id, data)
        progress_bar(i + 1, len(all_other), prefix="Channels", suffix=f"{ch['name']}")
    print()

    if emojis:
        cprint(f"\n  {C['yellow']}[*] Cloning Emojis ({len(emojis)})...{C['reset']}")
        for i, emoji in enumerate(emojis):
            if emoji.get("require_colons", True) and emoji.get("available", True):
                try:
                    img_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.png"
                    img_r = requests.get(img_url, headers=get_headers(token))
                    if img_r.status_code == 200:
                        img_b64 = base64.b64encode(img_r.content).decode("utf-8")
                        img_data = f"data:image/png;base64,{img_b64}"
                        create_guild_emoji(token, target_id, emoji["name"], img_data)
                except:
                    pass
            progress_bar(i + 1, len(emojis), prefix="Emojis", suffix=f":{emoji['name']}:")
        print()

    cprint(f"\n  {C['yellow']}[*] Applying server settings...{C['reset']}")
    settings = {}
    for key in ["name", "description", "system_channel_id", "afk_channel_id",
                 "afk_timeout", "verification_level", "default_message_notifications",
                 "explicit_content_filter", "mfa_level"]:
        if key in source:
            settings[key] = source[key]

    if source.get("icon"):
        cprint("  [*] Cloning server icon...", "yellow")
        try:
            icon_ext = "gif" if source["icon"].startswith("a_") else "png"
            icon_url = f"https://cdn.discordapp.com/icons/{source_id}/{source['icon']}.{icon_ext}?size=1024"
            icon_r = requests.get(icon_url, headers=get_headers(token))
            if icon_r.status_code == 200:
                icon_data = base64.b64encode(icon_r.content).decode("utf-8")
                settings["icon"] = f"data:image/{icon_ext};base64,{icon_data}"
                cprint("  [OK] Server icon captured!", "green")
        except:
            cprint("  [!] Could not clone server icon", "yellow")
    if target_name:
        settings["name"] = target_name
    if set_guild_settings(token, target_id, settings):
        cprint("  [OK] Server settings applied!", "green")
    else:
        cprint("  [!] Some settings could not be applied", "yellow")

    cprint(f"\n{C['green']}{C['bold']}")
    cprint("  +=========================================+")
    cprint("  |        CLONE COMPLETED SUCCESSFULLY!    |")
    cprint(f"  |  by {DEV_NAME:45s}|")
    cprint("  +=========================================+")
    cprint(f"{C['reset']}")
    input(f"\n  {C['dim']}Press Enter to return to menu...{C['reset']}")

async def clone_server(token, source_id, target_name=None):
    show_banner()
    cprint("  [*] Initializing clone operation...", "cyan", True)
    cprint("  [*] Fetching source server data...", "yellow")

    source = fetch_guild(token, source_id)
    if not source:
        cprint("  [X] Failed to fetch source server! Check the ID.", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    if target_name is None:
        target_name = f"{source['name']} Clone"

    cprint(f"\n  [Source] {source['name']} ({source_id})", "green")
    cprint(f"  [Target] {target_name}", "cyan")

    cprint(f"\n  {C['yellow']}[*] Creating target server...{C['reset']}")
    target_data, resp = create_guild(token, target_name)
    if not target_data:
        status = resp.status_code if resp is not None else 0
        cprint("  [X] Failed to create target server!", "red", True)
        try:
            err_msg = resp.json().get("message", resp.text) if resp is not None and resp.text else "No response"
        except Exception:
            err_msg = resp.text if resp is not None else "No response"
        cprint(f"  [X] HTTP {status}: {err_msg}", "red", True)
        if status == 429:
            cprint("  [!] Discord rate limit! Wait 10-15 min between creating servers.", "yellow")
        elif status in (400, 403):
            cprint("  [!] Discord rejected the request (needs phone verification / captcha / permission).", "yellow")
        else:
            cprint("  [!] Possible reasons:", "yellow")
            cprint("  - Token needs phone verification", "white")
            cprint("  - You already created 10+ servers (Discord limit)", "white")
        cprint(f"\n  {C['dim']}Try: Create the server manually in Discord, then use Option 4 (Clone to Existing){C['reset']}")
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return
    if isinstance(target_data, dict) and "id" not in target_data:
        cprint(f"  [X] API Error: {target_data}", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    target_id = target_data["id"]
    cprint(f"  [OK] Created server: {target_name} ({target_id})", "green", True)

    time.sleep(3)
    defaults = fetch_guild_channels(token, target_id) or []
    for ch in defaults:
        if ch.get("name") == "general":
            requests.delete(f"https://discord.com/api/v10/channels/{ch['id']}", headers=get_headers(token))
            break

    await clone_worker(token, source_id, target_id, source, target_name)

def verify_token(token):
    user = fetch_me(token)
    if user:
        guilds = fetch_guilds(token)
        gcount = len(guilds) if guilds else 0
        return user, gcount
    return None, 0

def token_menu():
    show_banner()
    cprint("  [Token Configuration]\n", "cyan", True)
    existing = load_token()
    if existing:
        cprint(f"  Current token: {C['dim']}{existing[:25]}...{C['reset']}", "yellow")
        cprint(f"  {C['dim']}  (saved in {TOKEN_FILE}){C['reset']}", "white")
        cprint(f"\n  {C['white']}[1]{C['reset']} Change Token")
        cprint(f"  {C['white']}[2]{C['reset']} Remove Token")
        cprint(f"  {C['white']}[3]{C['reset']} Back to Menu")
        choice = input(f"\n  {C['cyan']}> {C['reset']}").strip()
        if choice == "1":
            pass
        elif choice == "2":
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)
            cprint("  [OK] Token removed!", "green", True)
            time.sleep(1)
            return
        else:
            return

    cprint(f"\n  {C['yellow']}Enter your Discord token:{C['reset']}")
    token = input(f"  {C['cyan']}> {C['reset']}").strip()
    if not token:
        cprint("  [!] No token entered!", "yellow")
        time.sleep(1)
        return

    cprint("  [*] Verifying token...", "yellow")
    user, gcount = verify_token(token)
    if user:
        cprint(f"  [OK] Logged in as: {C['green']}{user['username']}#{user['discriminator']}{C['reset']}", "green", True)
        cprint(f"       Servers: {gcount}", "cyan")
        save_token(token)
    else:
        cprint("  [X] Invalid token! Check and try again.", "red", True)
    input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")

def show_token_info():
    show_banner()
    token = load_token()
    if not token:
        cprint("  [!] No token saved!", "yellow", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    user, gcount = verify_token(token)
    if user:
        cprint(f"  {C['bold']}Account Info:{C['reset']}\n", "cyan")
        cprint(f"  Username: {C['green']}{user['username']}#{user['discriminator']}{C['reset']}")
        cprint(f"  ID: {C['yellow']}{user['id']}{C['reset']}")
        cprint(f"  Email: {C['cyan']}{user.get('email', 'Hidden')}{C['reset']}")
        cprint(f"  Phone: {C['cyan']}{user.get('phone', 'None')}{C['reset']}")
        cprint(f"  MFA Enabled: {C['magenta']}{user.get('mfa_enabled', False)}{C['reset']}")
        cprint(f"  Servers: {C['white']}{gcount}{C['reset']}")
        cprint(f"  Avatar: {C['dim']}https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png{C['reset']}")
    else:
        cprint("  [X] Token is invalid or expired!", "red", True)
    input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")

def help_menu():
    show_banner()
    cprint(f"  {C['bold']}{C['white']}How to use {APP_NAME}:{C['reset']}\n", "cyan")
    cprint(f"  {C['yellow']}Step 1:{C['reset']} Set your Discord token (Option 2)")
    cprint(f"  {C['yellow']}Step 2:{C['reset']} Choose clone method:\n", "white")
    cprint(f"  {C['bold']}Option 1 (Clone Server):{C['reset']} Creates a NEW server and clones into it")
    cprint(f"  {C['bold']}Option 4 (Clone to Existing):{C['reset']} Clones INTO a server you already created\n")
    cprint(f"  {C['bold']}What it clones:{C['reset']}", "green")
    cprint(f"  - All roles with permissions & colors")
    cprint(f"  - All channels (Text, Voice, Categories)")
    cprint(f"  - Channel permissions")
    cprint(f"  - Server settings")
    cprint(f"  - Emojis")
    cprint(f"  - Stickers (if available)\n")
    cprint(f"  {C['bold']}Requirements:{C['reset']}", "yellow")
    cprint(f"  - Discord User Token (not bot token)")
    cprint(f"  - Source Server ID (right-click server > Copy ID)")
    cprint(f"  - For Option 4: Target Server ID (server must already exist)\n")
    cprint(f"  {C['bold']}Note:{C['reset']} {C['dim']}Option 4 will DELETE all channels/roles in the target server first!{C['reset']}")
    cprint(f"  {C['bold']}Note:{C['reset']} {C['dim']}Use responsibly! Server cloning may violate Discord ToS.{C['reset']}")
    cprint(f"\n  {C['bold']}Version:{C['reset']} {VERSION} | {C['bold']}Developer:{C['reset']} {DEV_NAME}\n")
    input(f"  {C['dim']}Press Enter to continue...{C['reset']}")

def clone_menu():
    show_banner()
    token = load_token()
    if not token:
        cprint("  [!] No token set! Go to Option 2 first.", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    user, gcount = verify_token(token)
    if not user:
        cprint("  [X] Token expired or invalid! Re-set it.", "red", True)
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    cprint(f"  Logged in as: {C['green']}{user['username']}#{user['discriminator']}{C['reset']}", "green", True)
    cprint(f"  Your servers: {gcount}\n", "cyan")

    cprint(f"  {C['yellow']}Enter Source Server ID:{C['reset']}")
    source_id = input(f"  {C['cyan']}> {C['reset']}").strip()
    if not source_id or not source_id.isdigit():
        cprint("  [X] Invalid ID! Must be a number.", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    cprint(f"\n  {C['yellow']}Enter target server name (or press Enter for default):{C['reset']}")
    target_name = input(f"  {C['cyan']}> {C['reset']}").strip()
    if not target_name:
        target_name = None

    cprint(f"\n  {C['red']}{C['bold']}  [!] WARNING: I'll create a new server. Continue? (y/n){C['reset']}")
    confirm = input(f"  {C['cyan']}> {C['reset']}").strip().lower()
    if confirm != "y":
        cprint("  [!] Cancelled.", "yellow")
        return

    asyncio.run(clone_server(token, source_id, target_name))

def clone_existing_menu():
    show_banner()
    token = load_token()
    if not token:
        cprint("  [!] No token set! Go to Option 2 first.", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    user, gcount = verify_token(token)
    if not user:
        cprint("  [X] Token expired or invalid! Re-set it.", "red", True)
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    cprint(f"  Logged in as: {C['green']}{user['username']}#{user['discriminator']}{C['reset']}", "green", True)
    cprint(f"  Your servers: {gcount}\n", "cyan")

    cprint(f"  {C['yellow']}Enter Source Server ID (the one to COPY FROM):{C['reset']}")
    source_id = input(f"  {C['cyan']}> {C['reset']}").strip()
    if not source_id or not source_id.isdigit():
        cprint("  [X] Invalid ID!", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    cprint(f"  {C['yellow']}Enter Target Server ID (the one to PASTE INTO):{C['reset']}")
    target_id = input(f"  {C['cyan']}> {C['reset']}").strip()
    if not target_id or not target_id.isdigit():
        cprint("  [X] Invalid ID!", "red", True)
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        return

    asyncio.run(clone_to_existing(token, source_id, target_id))

def main():
    try:
        while True:
            show_banner()
            show_menu()
            choice = input(f"\n  {C['cyan']}Choose option [1-6] > {C['reset']}").strip()
            if choice == "1":
                clone_menu()
            elif choice == "2":
                token_menu()
            elif choice == "3":
                show_token_info()
            elif choice == "4":
                clone_existing_menu()
            elif choice == "5":
                help_menu()
            elif choice == "6":
                cprint(f"\n  {C['green']}Goodbye! Thanks for using {APP_NAME} by {DEV_NAME}{C['reset']}", "cyan", True)
                sys.exit(0)
            else:
                cprint("  [!] Invalid choice!", "yellow")
                time.sleep(1)
    except KeyboardInterrupt:
        cprint(f"\n\n  {C['yellow']}Interrupted. Exiting...{C['reset']}")
        sys.exit(0)

if __name__ == "__main__":
    main()

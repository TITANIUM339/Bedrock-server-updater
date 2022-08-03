import os, re, sys, requests, platform
from zipfile import ZipFile


def main():
    print("Gathering resources...")

    # Current working directory.
    cwd = os.path.dirname(__file__)

    # Faking a browser visit because minecraft.net blocks python requests and wget etc.
    # List of User-Agent strings: http://www.useragentstring.com/pages/useragentstring.php.
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"}
    response = requests.get("https://www.minecraft.net/en-us/download/server/bedrock", headers=header)

    # Creating an HTML file and writing the web request content to it.
    open(os.path.join(cwd, "page.html"), "wb").write(response.content)
    
    # Opening the HTML file and extracting the minecraft-server link.
    with open(os.path.join(cwd, "page.html"), "r", encoding="utf8") as page:
        html = page.read()

        if platform.system() == "Windows":
            file_url = re.findall("https://minecraft.azureedge.net/bin-win/.*.zip", html)[0]
        else:
            file_url = re.findall("https://minecraft.azureedge.net/bin-linux/.*.zip", html)[0]
            
        file = re.findall("bedrock-server.*.zip", file_url)[0]

    # Checking if the latest minecraf-server zip file is already installed.
    if os.path.exists(os.path.join(cwd, file)):
        os.remove(os.path.join(cwd, "page.html"))
        sys.exit("You already have the latest version installed.")

    print("Updating bedrock-server... (this may take a while)")

    # Deleting the old minecraft-server zip file.
    for dir_file in os.listdir(cwd):
        if ".zip" in dir_file:
            os.remove(os.path.join(cwd, dir_file))

    # Deleting the HTML file
    os.remove(os.path.join(cwd, "page.html"))

    # Downloading the latest minecraft-server file.
    response = requests.get(file_url)
    open(os.path.join(cwd, file), "wb").write(response.content)

    # Extracting the minecraft-server zip file while not overwriting configuration files.
    with ZipFile(os.path.join(cwd, file),"r") as zip_ref:
        config_files = ("allowlist.json", "server.properties", "permissions.json")
        config_files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f)) and f in config_files]
        
        for member in zip_ref.namelist():
            if member not in config_files:
                zip_ref.extract(member, cwd)

    print("Update successful.")


if __name__ == "__main__":
    main()

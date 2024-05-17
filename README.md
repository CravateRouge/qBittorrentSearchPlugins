qBittorrent Search plugins
==========================

[OxTorrent](https://www.torrent911.vg) is a public french torrent search engine.

[yggtorrent](https://www.ygg.re/auth/login) is a semi-private french tracker that is specialized in high-quality and well-seeded torrents.

| :warning: WARNING          |
|:---------------------------|
| Your default DNS can block access to torrent websites. Use Google or Cloudflare DNS instead |
| The YggTorrent plugin is partially working because of the cloudflare DDOS protection see also [#10](/../../issues/10) |



Installation
------------
### OxTorrent

Download the [plugin file](oxtorrent.py) or copy the following [link](https://raw.githubusercontent.com/CravateRouge/qBittorrentSearchPlugins/master/oxtorrent.py).

After you've done this, you can add this plugin to qBittorrent by doing:

<kbd>Search tab</kbd> 🡪 <kbd>Search Plugins</kbd> 🡪 <kbd>Install a new one</kbd> 🡪 <kbd>Local File</kbd> then select the plugin file.
 **or**
<kbd>Web Link</kbd> then insert the link you copied.

Or manually copying the `oxtorrent.py` to the following location:
  * Linux: `~/.local/share/qBittorrent/nova3/engines/oxtorrent.py`
  * Mac: ``~/Library/Application Support/qBittorrent/nova/engines/oxtorrent.py`
  * Windows: `%localappdata%\qBittorrent\nova3\engines\oxtorrent.py`
  
### YggTorrent

Download the [plugin file](yggtorrent.py) or copy the following [link](https://raw.githubusercontent.com/CravateRouge/qBittorrentSearchPlugins/master/yggtorrent.py).

Because YggTorrent requires your login info, this plugin requires a bit more work than the one above.

1. Firstly, you need an [account](https://www3.yggtorrent.do/user/register)

2. Then you need to put your login information directly into the [plugin file](yggtorrent.py):

You can do this by editing these specific lines (lineno. 40:56).
```python
    # Login information ######################################################
    #
    # SET THESE VALUES!!
    #
    username = "YOUR USERNAME"
    password = "YOUR PASSWORD"
    ##########################################################################
    ...
```
Replace `YOUR USERNAME` and `YOUR PASSWORD` with *your* username and password, surrounded by quotation marks.  
For example, if your username is `foobar` and your password is `bazqux`:
```python
    ...
    # SET THESE VALUES
    #
    username = "foobar"
    password = "bazqux"
    ...
```
When this is done, you can follow the same steps as with the other plugin.

F.A.Q
-----

1. **This plugin doesn't require my torrent pass, does this plugin provide personalized torrents?**

  Because the plugin logs you in for every search, this means that the torrent files you open using it are your
  personal ones. It's effectively no different than if you'd visit the site and download the torrent manually.

2. **PROXY mode may had issue with search engine**

  While using a tor relay with a socks proxy mode, you may get no results form search engines request.
  Setting the Poxy Mode to SOCKS4 may fix this issue. You may also use SOCKS5 but have to enable "use only for torrents" option.



Thanks to [MadeOfMagicAndWires](https://github.com/MadeOfMagicAndWires) for the README template

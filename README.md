qBittorrent Search plugins
==========================

[yggtorrent.is](https://www1.yggtorrent.is) is a french semi-private tracker that specialises in high-quality,
well-seeded torrents.

Installation
------------

### YggTorrent
Download the [plugin file](yggtorrent.py) or copy the
following [link](https://raw.githubusercontent.com/CravateRouge/qBittorrentSearchPlugins/master/yggtorrent.py).

Because YggTorrent requires your login info, this plugin requires a bit more work than most.

1. Firstly you'll need an [account](https://ww1.yggtorrent.is/user/register)

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
Now replace the "YOUR USERNAME" and "YOUR PASSWORD" with *your* username and password, surrounded by quotation marks.  
So if your username is `foobar` and your `password` is bazqux these lines should read:
```python
    ...
    # SET THESE VALUES
    #
    username = "foobar"
    password = "bazqux"
    ...
```

After you've done this you can add this plugin to qBittorrent by going:

<kbd>Search tab</kbd> 🡪 <kbd>Search Plugins</kbd> 🡪 <kbd>Install a new one</kbd>  
<kbd>Local File</kbd> then select the plugin file
 **or**
<kbd>Web Link</kbd> then insert the link you copied.

Or by manually copying the `yggtorrent.py` to the following location:
  * Linux: `~/.local/share/data/qBittorrent/nova/engines/yggtorrent.py`
  * Mac: ``~/Library/Application Support/qBittorrent/nova/engines/yggtorrent.py`
  * Windows: `C:\Documents and Settings\username\Local Settings\Application Data\qBittorrent\nova\engines\yggtorrent.py`

F.A.Q
-----

1. **This plugin doesn't require my torrent pass, does this plugin provide personalized torrents?**

  Because the plugin logs you in for every search, this means that the torrent files you open using it are your
  personal ones. It's effectively no different than if you'd visit the site and download the torrent manually.



Thanks to [MadeOfMagicAndWires](https://github.com/MadeOfMagicAndWires) for the README template

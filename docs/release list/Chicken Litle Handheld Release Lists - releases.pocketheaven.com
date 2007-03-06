<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head><title>Handheld Release Lists - releases.pocketheaven.com</title>






<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

<link href="Chicken%20Litle%20Handheld%20Release%20Lists%20-%20releases.pocketheaven_files/releases.css" rel="stylesheet" type="text/css">
<link rel="alternate" type="application/rss+xml" title="All Releases RSS (Latest 5 GBA, NDS &amp; PSP)" href="http://releases.pocketheaven.com/all.rss.php">
<link rel="alternate" type="application/rss+xml" title="GBA Release RSS (Latest 10)" href="http://releases.pocketheaven.com/gba.rss.php">
<link rel="alternate" type="application/rss+xml" title="NDS Release RSS (Latest 10)" href="http://releases.pocketheaven.com/nds.rss.php">
<link rel="alternate" type="application/rss+xml" title="PSP Release RSS (Latest 10)" href="http://releases.pocketheaven.com/psp.rss.php"><!-- Sunbelt Kerio Popup Killer - script has been inserted by KPF -->



<script type="text/javascript">
<!--
var NoPopupsDone = 0;var CurrWindowOpen = window.open;var CurrWindowOpen2 = window.open;var orig_setTimeout = window.setTimeout;var orig_setInterval = window.setInterval;if ( window.showModelessDialog ) { var orig_showModelessDialog = window.showModelessDialog;} if ( window.showModalDialog ) { var orig_showModalDialog = window.showModalDialog;} 
var cnt = 0;var popupType = "direct";var KPF_LOG_URL = "http://127.0.0.1:44501/pl.html?";var KPF_TIMEOUT = 100;var onUnloadFlag = false;var KPF_CompleteLoaded = false;
function nullMethod() {}function nullWindow() {	 this.window = new Object(); this.document = new Object(); this.document.open=this.document.close=this.document.write=this.document.writeln=nullMethod; this.alert=this.back=this.blur=this.captureEvents=this.clearInterval=this.clearTimeout=this.close=this.confirm=this.dump=this.escape=this.focus=this.forward=this.GetAttention=this.getSelection=this.home=this.moveBy=this.moveTo=this.open=this.print=this.prompt=this.releaseEvents=this.resizeBy=this.resizeTo=this.scroll=this.scrollBy=this.scrollByLines=this.scrollByPages=this.scrollTo=this.setCursor=this.setInterval=this.setTimeout=this.sizeToContent=this.stop=this.unescape=this.updateCommands=nullMethod;}
function destroyIframe(ifr){ if (ifr != document.getElementById("kpfLogFrame"))   { var x = ifr.parentNode.removeChild(ifr);    delete x;  };}
function sendStream(s, idx, kpf_pt){ try {        var ifr = document.getElementById("kpfLogFrame");   var tmp = ifr.cloneNode(true);   tmp.id  = "ifr_" + idx;   var s2 = "srv=" + document.location + "&url=" + s + "&pty=" + kpf_pt;   tmp.src = KPF_LOG_URL + escape(s2);   document.body.appendChild(tmp); } catch (e) {   orig_setTimeout("sendStream('" + s + "', " + idx + ",'" + kpf_pt + "')", KPF_TIMEOUT); }}
function sendUrl(url){ if (onUnloadFlag)   sendStream(url, cnt++, popupType); else  {  try {   orig_setTimeout("sendStream('" + url + "', cnt++,'" + popupType + "')", KPF_TIMEOUT);  }   catch (e)   {}	  }}
function newOpen(url, name, atr) {wnd = new nullWindow();wnd.focus = nullWindow;wnd.opener = this.window;sendUrl(url);return(wnd); }
function newOpen2(url, name, atr) { sendUrl(url); return(new nullWindow());}
function stopPopups(kpf_pt) { popupType = kpf_pt; CurrWindowOpen = window.open; window.open = newOpen2; }
function startPopups(kpf_pt) { window.open = CurrWindowOpen;  popupType = kpf_pt;}
function my_setTimeout(one, two) { if (typeof(one) == "function") {    function myFun(){}    myFun=one;    function newFun() {     stopPopups('ontimer');      myFun();      startPopups('direct');    }	    try {      return orig_setTimeout(newFun,two);    }    catch (e)  {      try {	    return eval("newFun()");      }      catch(e) { }    }   }  else {    try {      return orig_setTimeout("stopPopups('ontimer');"+one+"; startPopups('direct');", two);    }    catch (e)  {      try {        return eval("stopPopups('ontimer');"+one+"; startPopups('direct');");      }      catch(e) { }    }  }}
function my_setInterval(one, two) {  if (typeof(one) == "function") {    function myFun(){}    myFun=one;    function newFun() {      stopPopups('ontimer');      myFun();      startPopups('direct');    }	    try {      return orig_setInterval(newFun,two);    }    catch (e) { }  }  else {    try {      return orig_setInterval("stopPopups('ontimer');"+one+";startPopups('direct');", two);    }     catch (e) { }  }}
function my_onload() { var my_retcode = true; stopPopups("onload"); if(orig_onload)  my_retcode = orig_onload(); startPopups("direct"); KPF_CompleteLoaded = true; return my_retcode; }
function my_unload() {  var my_retcode = true; var cnt = 0; stopPopups("onunload"); onUnloadFlag = true; if(orig_onunload)   my_retcode = orig_onunload(); startPopups("direct"); return my_retcode;}
function my_windowopen(url, name, atr){ if ( (! KPF_CompleteLoaded) || (document.all && event != null && event.type == "mouseover") )  {  if ( ! KPF_CompleteLoaded) {   popupType = "direct";  }  else {   popupType = "mouseover";  }  sendUrl(url);  popupType = "direct"; } else {   try {   return CurrWindowOpen2(url, name, atr);  }   catch (e)   {}  }}
function my_showModelessDialog (url , arguments , features) { if (!NoPopupsDone) {   var wnd = new nullWindow();  popupType = "direct_dialog";  sendUrl(url);  popupType = "direct";  return wnd; } if (popupType!="direct" | (event && event.type == "mouseover") ) {   var curr_popup = popupType;  if (event && event.type == "mouseover") {   popupType = "mouseover";  }    popupType = popupType+"_dialog";  sendUrl(url);  popupType = curr_popup;  return ( new nullWindow() ); } else {   return ( orig_showModelessDialog(url , arguments , features) );  } }
function my_showModalDialog (url , arguments , features) { if (!NoPopupsDone) {   popupType = "direct_dialog";  sendUrl(url);  popupType = "direct";  return ""; } if (popupType!="direct" | (event && event.type == "mouseover") ) {   var curr_popup = popupType;  if (event && event.type == "mouseover") {   popupType = "mouseover";  }    popupType = popupType+"_dialog";  sendUrl(url);  popupType = curr_popup;  return ""; } else {   return ( orig_showModalDialog(url , arguments , features) );  } }
function nopopups() { if(!NoPopupsDone)   {  NoPopupsDone = 1;  orig_onload = window.onload;  orig_onunload = window.onunload;  window.onload = my_onload;  window.onunload = my_unload;  window.open = my_windowopen;  }}
window.setTimeout = my_setTimeout;window.setInterval = my_setInterval;window.open = newOpen;if ( orig_showModelessDialog ) { window.showModelessDialog = my_showModelessDialog;}if ( orig_showModalDialog ) { window.showModalDialog = my_showModalDialog;}
//-->
</script><!-- Sunbelt Kerio Popup Killer - end of the script inserted by KPF -->

<script language="JavaScript">
<!--
   if (top != self) {
   top.location.href='http://releases.pocketheaven.com/';
   }
//-->
</script></head><body alink="#000000" bgcolor="#ffffff" link="#000000" text="#000000" vlink="#000000">

<table class="text" valign="top" align="center" border="0" cellpadding="2" cellspacing="2" width="700">
  <tbody><tr> 
    <td class="text" nowrap="nowrap"><a href="http://releases.pocketheaven.com/">
    <h1><b><center>Release Lists</center></b></h1>
  </a></td></tr>

  <tr>
    <td valign="top">

<center>
<table class="text" border="0" cellpadding="2" cellspacing="0" width="90%">
<tbody><tr class="text4" align="center" valign="middle"> 
<td bgcolor="#cccccc" nowrap="nowrap"><b>[</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://releases.pocketheaven.com/?system=gba&amp;section=release_list" class="text4"><b>GameBoy Advance</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://releases.pocketheaven.com/?system=nds&amp;section=release_list" class="text4"><b>Nintendo DS</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://releases.pocketheaven.com/?system=psp&amp;section=release_list" class="text4"><b>PSP</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>

<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://boards.pocketheaven.com/" class="text4"><b>Forum</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>]</b></td>
</tr>
</tbody></table>

<table class="text" border="0" cellpadding="2" cellspacing="0" width="90%">
<tbody><tr class="text4" align="center" valign="middle"> 
<td bgcolor="#cccccc" nowrap="nowrap"><b>[</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://releases.pocketheaven.com/?system=gbc&amp;section=release_list" class="text4"><b>GameBoy Color</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://releases.pocketheaven.com/?system=ws&amp;section=release_list" class="text4"><b>WonderSwan</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://bubbz.pocketheaven.com/" class="text4"><b>Patches</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://wiki.pocketheaven.com/" class="text4"><b>Wiki</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>]</b></td>
</tr>
</tbody></table>


Pocketheaven Sponsors:

<table class="text" border="0" cellpadding="2" cellspacing="0" width="90%">
<tbody><tr class="text4" align="center" valign="middle"> 

<td bgcolor="#cccccc" nowrap="nowrap"><b>[</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://www.jandaman.com/Merchant2/merchant.mvc?Screen=SFNT&amp;Store_Code=JIVGA&amp;AFFIL=6ql38ODD" class="text4"><b>Jandaman</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://www.linker4u.com/affiliatewiz/aw.asp?B=157&amp;A=246&amp;Task=Click" class="text4"><b>Linker4U</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<!-- <td nowrap bgcolor="#cccccc" width="25%"><A href="http://www.aheadgames.com/xcart/customer/home.php?partner=exile90@pocketheaven.com"><b>Ahead Games</b></A><strike></strike></td> -->
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://www.lik-sang.com/list.php?category=252&amp;lsaid=36759"><b>Lik-Sang</b></a><strike></strike></td>
<td bgcolor="#cccccc" nowrap="nowrap"><b>|</b></td>
<td bgcolor="#cccccc" nowrap="nowrap" width="25%"><a href="http://www.divineo.com/php/affstart.php?affcode=pocketh&amp;prod="><b>Divineo</b></a><strike></strike></td>
<!-- <td nowrap bgcolor="#cccccc" width="25%"><A HREF="http://www.play-asia.com/SOap-23-83-rp7-71-99.html"><b>Play-Asia</b></A><strike></strike></td> -->
<td bgcolor="#cccccc" nowrap="nowrap"><b>]</b></td>

</tr>
</tbody></table>



</center>	
	  </td>
  </tr>
</tbody></table>







<br>
<table class="text" valign="top" border="0" cellpadding="0" cellspacing="0" width="100%">

<tbody><tr align="left" valign="top"><td colspan="2" class="text4" bgcolor="#cccccc"><b>



0693 - Chicken Little - Ace In Action
</b></td>

</tr><tr><td valign="top" width="100%">


<table class="text" valign="top" align="left" border="0" cellpadding="0" cellspacing="0" width="100%">

<tbody><tr><td colspan="2" class="text"><b>Game Info:</b></td>
</tr><tr><td>System</td><td>Nintendo DS</td></tr>
<tr><td>Publisher</td><td>Buena Vista</td></tr>
<tr><td>Country</td><td>Europe</td></tr>
<tr><td>Language</td><td>Multi 5</td></tr>
<tr><td>Genre</td><td>Action</td></tr>
<tr><td>Date</td><td>n/a</td></tr>

<tr valign="top"><td>JDB Info</td><td>n/a</td></tr>

<tr><td colspan="2" class="text"><b>Dump Info:</b></td></tr>
<tr><td>Group</td><td>Legacy</td></tr>

<tr><td>Dirname</td><td>Chicken_Little_2_Ace_In_Action_EUR_NDS-LGC</td></tr>
<tr><td>Filename</td><td>lgc-cl2.zip</td></tr>

<tr><td>Date</td><td>2006-11-17</td></tr>

<tr><td colspan="2" class="text"><b>Internal Info:</b></td></tr>
<tr><td>Internal Name</td><td>CLACEACTION</td></tr>
<tr><td>Serial</td><td>NTR-AC4P-EUR</td></tr>
<tr><td>Version</td><td>1.0</td></tr>
<tr><td>Checksum</td><td>n/a</td></tr>
<tr><td>Complement</td><td>n/a</td></tr>
<tr><td>CRC32</td><td>25E220C1h</td></tr>
<tr><td>Size</td><td>512 Mbit</td></tr>
<tr><td>Save Type</td><td>EEPROM (4Kbit)</td></tr>



<tr><td colspan="2" class="text"><b>Extra Info:</b></td></tr>

<tr valign="top"><td>Release Notes</td><td>n/a</td></tr>


<tr valign="top"><td>Patches</td><td>n/a </td></tr>

<tr><td colspan="2" align="center">
<br>
<img src="Chicken%20Litle%20Handheld%20Release%20Lists%20-%20releases.pocketheaven_files/showimage.png" border="1"><p><a href="http://releases.pocketheaven.com/release/nds/914">&lt;&lt;</a> - <a href="http://releases.pocketheaven.com/release/nds/916">&gt;&gt;</a></p></td></tr></tbody></table>


</td><td valign="top">

<table class="text" valign="top" align="left" border="0" cellpadding="0" cellspacing="0" width="240">

<tbody><tr><td align="center">
<br>

<img src="Chicken%20Litle%20Handheld%20Release%20Lists%20-%20releases.pocketheaven_files/showimage_002.png" border="1"><br>&nbsp;<br>
<img src="Chicken%20Litle%20Handheld%20Release%20Lists%20-%20releases.pocketheaven_files/showimage_003.png" border="1">
<br>

<a href="http://releases.pocketheaven.com/boxart/nds/0915" class="text">Box Art</a><br>

<a href="http://releases.pocketheaven.com/nfoview/nds/0915" class="text">NFO</a>


</td></tr></tbody></table>


</td></tr></tbody></table>




<p>
</p><center>
<table class="text">
  <tbody><tr align="center" valign="bottom"> 
    <td>Copyright © 2003-2005 <a href="http://releases.pocketheaven.com/?section=about">releases.pocketheaven.com</a> - Code by Exile`90 used with permission<br>Hosting provided by <a href="http://www.noemitm.ca/">noemitm.ca</a></td></tr>



  <tr align="center" valign="bottom"> 
    <td>

<script type="text/javascript"><!--
google_ad_client = "pub-9018007347516008";
google_alternate_color = "FFFFFF";
google_ad_width = 468;
google_ad_height = 60;
google_ad_format = "468x60_as";
google_ad_type = "text";
google_ad_channel ="6160377614";
google_page_url = document.location;
google_color_border = "CCCCCC";
google_color_bg = "FFFFFF";
google_color_link = "000000";
google_color_url = "666666";
google_color_text = "333333";
//--></script>
<script type="text/javascript" src="Chicken%20Litle%20Handheld%20Release%20Lists%20-%20releases.pocketheaven_files/show_ads.js">
</script><iframe name="google_ads_frame" src="Chicken%20Litle%20Handheld%20Release%20Lists%20-%20releases.pocketheaven_files/ads.htm" marginwidth="0" marginheight="0" vspace="0" hspace="0" allowtransparency="true" frameborder="0" height="60" scrolling="no" width="468"></iframe>

</td></tr>
</tbody></table>

</center>

<!-- Sunbelt Kerio Popup Killer - script has been appended by KPF -->
<iframe id="kpfLogFrame" src="Chicken%20Litle%20Handheld%20Release%20Lists%20-%20releases.pocketheaven_files/pl.htm" onload="destroyIframe(this)" style="display: none;">
</iframe>
<script type="text/javascript">
<!--
	nopopups();
//-->
</script>
<!-- Sunbelt Kerio Popup Killer - end of the script appended by KPF-->
</body></html>
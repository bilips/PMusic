var text = "<p>Ready</p>";

var main = "<div class='main'>";
    main += "<div class=\"title\">\n";
    main += "  <p><img src=\"./icon.svg\" width=\"100\" />PMusic<\/p>\n";
    main += "<\/div>\n";
    main += "<div class=\"content\">\n";
    main += "  <input placeholder=\"输入要搜索歌曲的名称\" id=\"music_name\" />\n";
    main += "  <button class=\"search-btn\" onclick=\"search()\">搜索<\/button>\n";
    main += "<\/div>\n";
    main += "<\/div>\n";

var player = "";
    player += "<div class=\"result\">\n";
    player += "  <button class=\"back-btn\" onclick='back();'>返回<\/button>\n";
    player += "  <div class=\"content\">\n";
    player += "    <div id=\"aplayer\"><\/div>\n";
    player += "  <\/div>\n";
    player += "<\/div>\n";
    player += "\n";

// 歌曲url
var songurl = []

// 加载搜索界面
window.onload = function(){
    var body = document.getElementById("body");
    body.innerHTML = main;
};

function set_text(){
    var info = document.getElementById("info");
    info.innerHTML = text;
}

function back(){
    var body = document.getElementById("body");
    body.innerHTML = main;
    text = "<p>Ready</p>";
    set_text();
}

function search(){
    var music_name = document.getElementById("music_name").value;
    if(music_name.replace(/\s+/g,"") == ""){
        alert("请输入音乐名称!");
    }
    else{
        // 设置结果界面
        var body = document.getElementById("body");
        body.innerHTML = player;
        text = "";
        text += "<p>获取链接列表...";
        set_text();
        get_urls(music_name);
    }
}

async function get_urls(music_name){
    var content = await eel.search(music_name)();
    text += "完成！</p><p>获取内容信息...";
    set_text();
    // 获取详细信息
    var audio = await eel.get_data(content)();
    text += "完成！</p><p>设置Aplayer...";
    set_text();
    // Aplayer
    if(audio.length){
        const ap = new APlayer({
            container: document.getElementById('aplayer'),
            mini: false,
            autoplay: false,
            theme: '#b7daff',
            loop: 'all',
            order: 'list',
            preload: 'auto',
            volume: 0.7,
            mutex: true,
            listFolded: false,
            listMaxHeight: "250px",
            lrcType: 2,
            audio: audio
        });
    }
    else{
        var info = document.getElementById("aplayer");
        info.innerHTML = "啥都木有～";
    }
    text = "<p>完成力!</p>";
    set_text();
}
var sPlayer;
var sCurrentEntry;

function main() {
    initPlaylistEntries();
    initPlayer();
}

function initPlayer() {
    sPlayer = $("#player")[0];
    sPlayer.addEventListener("ended", goToNext);

    var firstEntry = $(".playlist-entry")[0];
    if (!firstEntry) {
        $(sPlayer).hide();
        return;
    }
    setCurrentEntry(firstEntry);
}

function initPlaylistEntries() {
    $(".play-indicator").hide();
    $(".entry-link").click(function() {
        setCurrentEntry(this.parentElement);
        sPlayer.play();
    });
}

function setCurrentEntry(entry) {
    if (sCurrentEntry) {
        $(sCurrentEntry).find(".play-indicator").hide();
    }
    sCurrentEntry = entry;
    if (!sCurrentEntry) {
        return;
    }
    var rawUrl = entry.getAttribute("data-raw-url");
    sPlayer.setAttribute("src", rawUrl);
    $("#song-name").html(sCurrentEntry.getAttribute("data-name"));
    $(entry).find(".play-indicator").show();
}

function goToNext() {
    var entry = $(sCurrentEntry).next(".playlist-entry")[0];
    if (entry) {
        setCurrentEntry(entry);
        sPlayer.play();
    }
}

var sPlayer;
var sCurrentEntry;

function main() {
    initPlaylistEntries();
    initPlayer();
    initPlayerUi();
}

function initPlayer() {
    sPlayer = $("#audio")[0];
    sPlayer.addEventListener("loadedmetadata", updateSongDuration);
    sPlayer.addEventListener("play", updatePlayButton);
    sPlayer.addEventListener("pause", updatePlayButton);
    sPlayer.addEventListener("ended", updatePlayButton);
    sPlayer.addEventListener("ended", goToNext);
    sPlayer.addEventListener("timeupdate", updatePlayerSlider);

    var firstEntry = $(".playlist-entry")[0];
    if (!firstEntry) {
        $("#player").hide();
        return;
    }
    setCurrentEntry(firstEntry);
}

function initPlayerUi() {
    $("#player-prev").click(goToPrev);
    $("#player-play").click(onPlayClicked);
    $("#player-next").click(goToNext);
    $("#player-slider").slider({
        start: onSliderStarted,
        stop: onSliderStopped
    });
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

function goToPrev() {
    var entry = $(sCurrentEntry).prev(".playlist-entry")[0];
    if (entry) {
        setCurrentEntry(entry);
        sPlayer.play();
    }
}

function onPlayClicked() {
    if (sPlayer.paused) {
        sPlayer.play();
    } else {
        sPlayer.pause();
    }
}

function updatePlayButton() {
    var button = $("#player-play");
    if (sPlayer.paused) {
        button.html("▶");
    } else {
        button.html("||");
    }
}

function updateSongDuration() {
    var duration = sPlayer.duration;
    var minutes = Math.floor(duration / 60).toString();
    var seconds = Math.floor(duration % 60).toString();
    if (seconds.length == 1) {
        seconds = "0" + seconds;
    }
    var txt = minutes + ":" + seconds;
    $("#song-duration").html(txt);
    $("#player-slider").slider("option", "max", duration);
}

var sSliding = false;
function updatePlayerSlider() {
    if (sSliding) {
        return;
    }
    $("#player-slider").slider("value", sPlayer.currentTime);
}

function onSliderStarted(event, ui) {
    sSliding = true;
}

function onSliderStopped(event, ui) {
    sSliding = false;
    sPlayer.currentTime = ui.value;
}

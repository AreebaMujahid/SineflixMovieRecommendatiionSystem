var height = 6; //number of guesses
var width = 5; //length of the word

var row = 0; //current guess (attempt #)
var col = 0; //current letter for that attempt

var gameOver = false;
var guessList = []; // Initialize guessList

var wordList = ["action", "actor", "actress", "adventure", "alien", "animated", "award", "backstage", "blockbuster", "boxoffice", "camera", "cast", "casting", "character", "cinema", "cinematography", "classic", "comedy", "costume", "critic", "cut", "director", "drama", "dubbing", "effects", "emotions", "ending", "entertainment", "epic", "extra", "fantasy", "feature", "fiction", "film", "filming", "genre", "grip", "hero", "hollywood", "horror", "iconic", "imagination", "improvise", "interview", "lighting", "makeup", "marquee", "masterpiece", "matinee", "motion", "movie", "mystery", "narrative", "nominee", "opening", "original", "oscar", "outtake", "performance", "plot", "popcorn", "premiere", "producer", "projection", "prologue", "rating", "reel", "remake", "role", "scene", "script", "sequel", "set", "shot", "sound", "special", "star", "stunt", "studio", "subtitles", "suspense", "take", "teaser", "technique", "thriller", "title", "trailer", "tribute", "trope", "twist", "villain", "visual", "voiceover", "war", "wardrobe", "western", "zombie", "zoom", "academy", "action-packed", "adaptation", "aerial", "agent", "alienation", "ambience", "angle", "anthology", "apocalypse", "appraisal", "artistic", "assembly", "atmosphere", "audience", "award-winning", "background", "backlot", "behind-the-scenes", "blockbuster", "bluescreen", "camera", "cameo", "captivating", "capture", "cartoon", "celebrity", "chase", "cinematographer", "climax", "comedian", "comical", "commercial", "conflict", "confrontation", "convention", "costume", "counterfeit", "crane", "credits", "critique", "cult", "cult-favorite", "cutting-room", "daring", "dazzling", "debut", "dialogue", "director's-cut", "disguise", "disney", "dolly", "documentary", "dolly-shot", "drama", "dramatic", "dubbed", "dystopian", "edgy", "editing", "emotions", "ensemble", "epic", "establishing", "exposition", "extra", "extraterrestrial", "fade-in", "fade-out", "fantasy", "fashion", "feature-length", "fictional", "figurine", "filmed", "filmmaker", "flashback", "flash-forward", "flawless", "focus", "footage", "foreign", "frame", "futuristic", "gaffer", "genre", "ghost", "gory", "green-screen", "gripping", "gunshot", "harsh", "heartwarming", "heroic", "historical", "hollywood", "horror", "iconic", "illusion", "imagination", "improv", "indie", "ingenious", "insightful", "inspiring", "intense", "intriguing", "juxtaposition", "killer", "landmark", "lens", "lifelike", "lighting", "make-up", "marathon", "masterpiece", "melodrama", "memorable", "montage", "motion", "moviegoer", "multicultural", "mysterious", "mythical", "narration", "narrative", "naturalistic", "neo-noir", "non-linear", "nostalgic", "nuanced", "nudity", "obsession", "opening", "orchestration", "over-the-top", "overcome", "panning", "parody", "performance", "period-piece", "perspective", "phenomenon", "photography", "plot", "point-of-view", "post-production", "premiere", "presenter", "prestigious", "production", "projector", "prologue", "prophetic", "protagonist", "provocative", "publicity", "puppet", "puzzle", "pyrotechnics", "quirky", "racy", "realism", "realistic", "reboot", "reception", "recognizable", "recreation", "rehearsal", "release", "remake", "rendition", "reputation", "resonate", "revenge", "revolutionary", "romantic", "satire", "scene", "sci-fi", "script", "screen", "screenplay", "screenwriter", "seamless", "sequel", "sequencing", "serious", "set", "setting", "shaky-cam", "shoot", "shooting", "short-film", "shot", "showcase", "silent", "silver-screen", "singer", "sketch", "slick", "slideshow", "smash-hit", "sound"];

guessList = guessList.concat(wordList);

var word = wordList[Math.floor(Math.random()*wordList.length)].toUpperCase();
console.log(word);

window.onload = function(){
    initialize();
}

function initialize() {
    // Create the game board
    for (let r = 0; r < height; r++) {
        for (let c = 0; c < width; c++) {
            let tile = document.createElement("span");
            tile.id = r.toString() + "-" + c.toString();
            tile.classList.add("tile");
            tile.innerText = "";
            document.getElementById("board").appendChild(tile);
        }
    }

    // Create the key board
    let keyboard = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", " "],
        ["Enter", "Z", "X", "C", "V", "B", "N", "M", "⌫"]
    ]

    for (let i = 0; i < keyboard.length; i++) {
        let currRow = keyboard[i];
        let keyboardRow = document.createElement("div");
        keyboardRow.classList.add("keyboard-row");

        for (let j = 0; j < currRow.length; j++) {
            let keyTile = document.createElement("div");
            let key = currRow[j];
            keyTile.innerText = key;
            if (key == "Enter") {
                keyTile.id = "Enter";
            }
            else if (key == "⌫") {
                keyTile.id = "Backspace";
            }
            else if ("A" <= key && key <= "Z") {
                keyTile.id = "Key" + key;
            } 

            keyTile.addEventListener("click", processKey);

            if (key == "Enter") {
                keyTile.classList.add("enter-key-tile");
            } else {
                keyTile.classList.add("key-tile");
            }
            keyboardRow.appendChild(keyTile);
        }
        document.body.appendChild(keyboardRow);
    }

    // Listen for Key Press
    document.addEventListener("keyup", (e) => {
        processInput(e);
    })
}

function processKey() {
    e = { "code" : this.id };
    processInput(e);
}

function processInput(e) {
    if (gameOver) return; 

    if ("KeyA" <= e.code && e.code <= "KeyZ") {
        if (col < width) {
            let currTile = document.getElementById(row.toString() + '-' + col.toString());
            if (currTile.innerText == "") {
                currTile.innerText = e.code[3];
                col += 1;
            }
        }
    }
    else if (e.code == "Backspace") {
        if (0 < col && col <= width) {
            col -=1;
        }
        let currTile = document.getElementById(row.toString() + '-' + col.toString());
        currTile.innerText = "";
    }
    else if (e.code == "Enter") {
        update();
    }

    if (!gameOver && row == height) {
        gameOver = true;
        document.getElementById("answer").innerText = word;
    }
}

function update() {
    let guess = "";
    document.getElementById("answer").innerText = "";

    //string up the guesses into the word
    for (let c = 0; c < width; c++) {
        let currTile = document.getElementById(row.toString() + '-' + c.toString());
        let letter = currTile.innerText;
        guess += letter;
    }

    guess = guess.toLowerCase(); //case sensitive

    if (!guessList.includes(guess)) {
        document.getElementById("answer").innerText = "Not in word list";
        return;
    }
    
    //start processing guess
    let correct = 0;
    let letterCount = {}; //keep track of letter frequency

    for (let i = 0; i < word.length; i++) {
        let letter = word[i];

        if (letterCount[letter]) {
            letterCount[letter] += 1;
        } 
        else {
            letterCount[letter] = 1;
        }
    }

    //first iteration, check all the correct ones first
    for (let c = 0; c < width; c++) {
        let currTile = document.getElementById(row.toString() + '-' + c.toString());
        let letter = currTile.innerText;

        //Is it in the correct position?
        if (word[c] == letter) {
            currTile.classList.add("correct");

            let keyTile = document.getElementById("Key" + letter);
            keyTile.classList.remove("present");
            keyTile.classList.add("correct");

            correct += 1;
            letterCount[letter] -= 1; //deduct the letter count
        }

        if (correct == width) {
            gameOver = true;
        }
    }

    //go again and mark which ones are present but in wrong position
    for (let c = 0; c < width; c++) {
        let currTile = document.getElementById(row.toString() + '-' + c.toString());
        let letter = currTile.innerText;

        // skip the letter if it has been marked correct
        if (!currTile.classList.contains("correct")) {
            //Is it in the word?         //make sure we don't double count
            if (word.includes(letter) && letterCount[letter] > 0) {
                currTile.classList.add("present");
                
                let keyTile = document.getElementById("Key" + letter);
                if (!keyTile.classList.contains("correct")) {
                    keyTile.classList.add("present");
                }
                letterCount[letter] -= 1;
            } // Not in the word or (was in word but letters all used up to avoid overcount)
            else {
                currTile.classList.add("absent");
                let keyTile = document.getElementById("Key" + letter);
                keyTile.classList.add("absent")
            }
        }
    }

    row += 1; //start new row
    col = 0; //start at 0 for new row
}

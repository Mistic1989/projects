
import Brain from "./brain";
import UI from "./ui";

function validateIndexHtml(): void {
    if (document.querySelectorAll("#app").length != 1) {
        throw Error("More or less than one div with id 'app' found!");
    }
    if (document.querySelectorAll("div").length != 1) {
        throw Error("More or less than one div found in index.html!");
    }
}

function initializeUI(ui: UI): void {
    ui.draw();
    window.addEventListener('resize', () => {
        uiDrawRepeater(ui);
    });
    uiDrawRepeater(ui);
}

function handleNameInput(ui: UI): void {
    let input: HTMLElement | null = document.getElementById("playerName");

    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                ui.getBrain.createPlayer(input.toString());
                uiDrawRepeater(ui);
            }
        });
    }
}

// Function to handle menu actions
function handleMenuActions(ui: UI): void {
    let start: HTMLElement | null = document.getElementById("start");
    if (start) {
        start.addEventListener('click', () => {
            ui.getBrain.startGame();
            ui.getBrain.movingBall();
            ui.getBrain.setToggleMenu = false;
            uiDrawRepeater(ui);
        });
    }
}

function handleCreateNewPlayer(ui: UI): void {
    let player: HTMLElement | null = document.getElementById("createPlayer");
    let start: HTMLElement | null = document.getElementById("start");
    let scoreTable: HTMLElement | null = document.getElementById("scoreTableButton");
    if (player && start && scoreTable) {
        player.addEventListener('click', () => {
            start.style.visibility = 'hidden';
            scoreTable.style.visibility = 'hidden';
            player.style.visibility = 'hidden';
            ui.drawNameInput();
            handleNameInput(ui);
        });
    }
}

function handleScoreTableButton(ui: UI): void {
    let scoreTable: HTMLElement | null = document.getElementById("scoreTableButton");
    let player: HTMLElement | null = document.getElementById("createPlayer");
    let start: HTMLElement | null = document.getElementById("start");
    console.log(scoreTable);

    if (player && start && scoreTable) {
        scoreTable.addEventListener('click', () => {

            start.style.visibility = 'hidden';
            player.style.visibility = 'hidden';
            scoreTable.style.visibility = 'hidden';
            console.log(ui.getBrain.scoreTable);
            ui.drawScoreTable(ui.getBrain);
            
        });
    }
}

function uiDrawRepeater(ui: UI): void {
    setTimeout(() => {
        ui.draw();
        // console.log(ui.brain.player.playerName);
        // console.log(ui.brain.player.id);
        // console.log(ui.brain.scoreTable);
        // console.log(ui.brain.ball.ballSpeed);
        // Check if user input is required

        // if (!ui.brain.toggleMenu) {
        //     document.addEventListener('keypress', (e) => {
        //         if (e,key === "l") {
        //             ui.brain.shootingBullet();
        //         }
        //     })
        // }
        if (ui.getBrain.bullet.getDrawBullet) {
            ui.drawBullet(ui.getBrain.bullet);
        }

        if (ui.getBrain.getGameOver) {
            ui.drawGameOver();
        }

        if (!ui.getBrain.getUserNameEntered) {
            ui.drawNameInput();
            handleNameInput(ui);
        }
        // Check if the menu is toggled
        else if (ui.getBrain.getToggleMenu) {
            ui.drawMenu(ui.getBrain);
            handleCreateNewPlayer(ui);
            handleScoreTableButton(ui);
            handleMenuActions(ui);
            
        }
        else {
            uiDrawRepeater(ui);
        }
    }, 0);
}


function main(): void {

    validateIndexHtml();
    let appDiv: HTMLDivElement | null = document.querySelector("#app");
    let brain: Brain = new Brain();
    let ui: UI = new UI(brain, appDiv!);
    initializeUI(ui);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'l' && !ui.getBrain.bullet.getDrawBullet && ui.getBrain.getShootingEnabled) {
            console.log("shoot");
            // ui.brain.shootingCountdown();
            ui.getBrain.bullet.setLeft = ui.getBrain.paddle.getLeft + (ui.getBrain.paddle.getWidth / 2);
            ui.getBrain.bullet.setTop = ui.getBrain.paddle.getTop;
            ui.getBrain.bullet.setDrawBullet = true;
            ui.getBrain.shootingBullet();
        }
        if (e.key === 'Escape') {
            ui.getBrain.setGameOver = false;
            ui.getBrain.toggleMenuVisible();
            ui.getBrain.ball.toggleballPause();
            if (ui.getBrain.ball.pause === false) {
                ui.getBrain.movingBall();
            } 
            uiDrawRepeater(ui);
        }

        if (e.key === 'a') {
            brain.startMovePaddle(brain.paddle, -1);
        }
        if (e.key === 'd') {
            brain.startMovePaddle(brain.paddle, 1);
        }
    });

    document.addEventListener('keyup', (e) => {
        switch (e.key) {
            case 'a':
                brain.stopMovePaddle(brain.paddle);
                break;
            case 'd':
                brain.stopMovePaddle(brain.paddle);
                break;
        }

    });

    uiDrawRepeater(ui);
}

main();
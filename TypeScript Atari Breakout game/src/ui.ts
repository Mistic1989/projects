import Brain, { Ball, Brick, Bullet, Paddle, Player } from "./brain";

export default class UI {

    width: number = -1;
    height: number = -1;

    startButton: HTMLButtonElement | null = null;

    private scaleX: number = 1;
    private scaleY: number = 1;

    constructor(private brain: Brain, private appContainer: HTMLDivElement) {
        // this.startButton = null;
        this.setScreenDimensions();
    }

    public get getBrain(): Brain {
        return this.brain;
    }

    setScreenDimensions(width?: number, height?: number): void {
        this.width = width || document.documentElement.clientWidth;
        this.height = height || document.documentElement.clientHeight;

        this.scaleX = this.width / this.brain.width;
        this.scaleY = this.height / this.brain.height;

    }

    calculateScaledX(x: number): number {
        return x * this.scaleX | 0;
    }

    calculateScaledY(y: number): number {
        return y * this.scaleY | 0;
    }

    drawBorderSingle(left: number, top: number, width: number, height: number, color: string) {
        let border: HTMLDivElement = document.createElement('div');

        border.style.zIndex = "10";
        border.style.position = 'fixed';

        border.style.left = left + 'px';
        border.style.top = top + 'px';

        border.style.width = width + 'px';
        border.style.height = height + 'px';
        border.style.backgroundColor = color;

        this.appContainer.append(border);
    }

    drawBorder(): void {
        // top border
        this.drawBorderSingle(0, 0, this.width, this.calculateScaledY(this.brain.borderThickness), 'grey');
        // left
        this.drawBorderSingle(0, 0, this.calculateScaledX(this.brain.borderThickness), this.height, 'grey');
        // right
        this.drawBorderSingle(this.width - this.calculateScaledX(this.brain.borderThickness), 0, this.calculateScaledX(this.brain.borderThickness), this.height, 'grey');
        this.drawBorderSingle(0, this.height - this.calculateScaledY(this.brain.borderThickness), this.width, this.calculateScaledY(this.brain.borderThickness), 'grey');
    }

    drawPaddle(paddle: Paddle) {
        let div: HTMLDivElement = document.createElement('div');

        div.style.zIndex = "10";
        div.style.position = 'fixed';

        div.style.left = this.calculateScaledX(paddle.getLeft) + 'px';
        div.style.top = this.calculateScaledY(paddle.getTop) + 'px';

        div.style.width = this.calculateScaledX(paddle.getWidth) + 'px';
        div.style.height = this.calculateScaledY(paddle.getHeight) + 'px';

        div.style.backgroundColor = paddle.getColor;

        this.appContainer.append(div);
    }

    drawBall(ball: Ball) {
        let div: HTMLDivElement = document.createElement('div');

        div.style.zIndex = "10";
        div.style.position = 'fixed';

        div.style.borderRadius = 50 + '%';
        div.style.left = this.calculateScaledX(ball.getLeft) + 'px';
        div.style.top = this.calculateScaledY(ball.getTop) + 'px';

        div.style.width = this.calculateScaledX(ball.width) + 'px';
        div.style.height = this.calculateScaledY(ball.height) + 'px';

        div.style.backgroundColor = ball.getColor;
        this.appContainer.append(div);
    }

    drawBullet(bullet: Bullet): void {
        let div: HTMLDivElement = document.createElement('div');

        div.style.zIndex = "10";
        div.style.position = 'fixed';

        div.style.left = this.calculateScaledX(bullet.getLeft) + 'px';
        div.style.top = this.calculateScaledY(bullet.getTop) + 'px';

        div.style.width = this.calculateScaledX(bullet.width) + 'px';
        div.style.height = this.calculateScaledY(bullet.height) + 'px';

        div.style.backgroundColor = bullet.getColor;

        this.appContainer.append(div);
    }

    drawScore(): void {
        let div: HTMLDivElement = document.createElement('div');

        div.textContent = "SCORE: " + this.brain.player.getScore;
        div.style.fontFamily = "DotGothic16";
        div.style.fontWeight = '400';
        div.style.fontStyle = 'normal';
        div.style.fontSize = this.calculateScaledX(20) + 'px';
        div.style.zIndex = "10";
        div.style.position = 'fixed';

        div.style.left = this.calculateScaledX(40) + 'px';
        div.style.top = this.calculateScaledY(300) + 'px';

        div.style.color = 'white';

        this.appContainer.append(div);
    }

    drawTurnsLeft(): void {
        let div: HTMLDivElement = document.createElement('div');

        div.textContent = "TURNS: " + this.brain.player.getTurns;
        // div.textContent = this.brain.shootingCountDownValue;
        div.style.fontFamily = "DotGothic16";
        div.style.fontWeight = '400';
        div.style.fontStyle = 'normal';
        div.style.fontSize = this.calculateScaledX(20) + 'px';
        div.style.zIndex = "10";
        div.style.position = 'fixed';

        div.style.left = this.calculateScaledX(40) + 'px';
        div.style.top = this.calculateScaledY(350) + 'px';

        div.style.color = 'white';

        this.appContainer.append(div);
    }

    drawLevel(): void {
        let div: HTMLDivElement = document.createElement('div');

        div.textContent = "LEVEL: " + this.brain.player.getLevel;
        div.style.fontFamily = "DotGothic16";
        div.style.fontWeight = '400';
        div.style.fontStyle = 'normal';
        div.style.fontSize = this.calculateScaledX(20) + 'px';
        div.style.zIndex = "10";
        div.style.position = 'fixed';

        div.style.left = this.calculateScaledX(40) + 'px';
        div.style.top = this.calculateScaledY(400) + 'px';

        div.style.color = 'white';

        this.appContainer.append(div);
    }

    drawShootingCountDown(): void {
        let div: HTMLDivElement = document.createElement('div');

        div.textContent = "SHOOTING ENBALED: " + this.brain.getShootingCountDownValue;
        div.style.fontFamily = "DotGothic16";
        div.style.fontWeight = '400';
        div.style.fontStyle = 'normal';
        div.style.fontSize = this.calculateScaledX(20) + 'px';
        div.style.zIndex = "10";
        div.style.position = 'fixed';

        div.style.left = this.calculateScaledX(40) + 'px';
        div.style.top = this.calculateScaledY(450) + 'px';

        div.style.color = 'white';

        if (this.brain.getShootingEnabled) {
            this.appContainer.append(div);
        }
    }


    drawBrick(brick: Brick): void {

        const rows: number = 2;
        const cols: number = 10;

        const totalWidth: number = (brick.getWidth * cols) + (brick.padding * (cols - 1));
        // const totalHeight = brick.height * 2 + (brick.padding * (2 - 1));
        const startX: number = ((this.brain.width) - totalWidth) / 2;
        
        for (let i = 0; i < this.brain.bricks.length; i++) {

            const currentBrick: Brick = this.brain.bricks[i];

            if (currentBrick.getVisible) {
                let div: HTMLImageElement = document.createElement('img');

                div.style.zIndex = "10";
                div.style.position = 'fixed';
    
                div.style.left = this.calculateScaledX(currentBrick.getLeft) + 'px';
                div.style.top = this.calculateScaledY(currentBrick.getTop) + 'px';
                div.style.width = this.calculateScaledX(currentBrick.getWidth) + 'px';
                div.style.height = this.calculateScaledY(currentBrick.getHeight) + 'px';
    
                div.style.backgroundColor = currentBrick.getColor;

                // let img = document.createElement('img');
                if (currentBrick.getImage != undefined) {

                    div.src = currentBrick.brickImageSrc;
                    div.width = currentBrick.getWidth;
                    div.height = currentBrick.getHeight;
                    // div.appendChild(img);
                }

                this.appContainer.append(div);
            }
        }
    }

    drawNameInput(): void {
        const label: HTMLLabelElement = document.createElement('label');
        label.textContent = 'Enter your name:';
        label.style.left = this.calculateScaledX(400) + 'px';
        label.style.top = this.calculateScaledY(300) + 'px';
        label.style.color = 'white';
        label.style.zIndex = "10";
        label.style.position = 'fixed';
        label.style.fontSize = this.calculateScaledX(35) + 'px';
        label.style.fontSize = this.calculateScaledY(35) + 'px';
        label.style.fontFamily = "DotGothic16";
        
        const input: HTMLInputElement = document.createElement('input');
        input.type = 'text';
        input.id = 'playerName';
        input.name = 'playerName';
        input.style.left = this.calculateScaledX(350) + 'px';
        input.style.top = this.calculateScaledY(400) + 'px';
        input.style.zIndex = "10";
        input.style.position = 'fixed';
        input.style.fontSize = this.calculateScaledX(35) + 'px';
        input.style.fontSize = this.calculateScaledY(35) + 'px';
        input.style.fontFamily = "DotGothic16";

        label.append(input);
        this.appContainer.append(label);
    }

    drawMenu(brain: Brain): void {

        const title: HTMLHeadingElement = document.createElement('h1');
        title.textContent = 'PRESS ENTER TO START GAME';
        title.style.fontFamily = "DotGothic16";
        title.style.left = this.calculateScaledX(400) + 'px';
        title.style.top = this.calculateScaledY(350) + 'px';
        title.style.fontSize = this.calculateScaledX(35) + 'px';
        title.style.fontSize = this.calculateScaledY(35) + 'px';
        title.style.zIndex = "10";
        title.style.color = 'red';
        title.style.position = 'fixed';
        

        this.startButton = document.createElement('button');
        this.startButton.textContent = 'Start New Game';
        this.startButton.id = 'start';
        this.startButton.style.left = this.calculateScaledX(400) + 'px';
        this.startButton.style.top = this.calculateScaledY(400) + 'px';
        this.startButton.style.fontSize = this.calculateScaledX(35) + 'px';
        this.startButton.style.fontSize = this.calculateScaledY(35) + 'px';
        this.startButton.style.zIndex = "20";
        this.startButton.style.position = 'fixed';


        const scoreTableButton: HTMLButtonElement = document.createElement('button');
        scoreTableButton.textContent = 'ScoreTable';
        scoreTableButton.id = 'scoreTableButton';
        scoreTableButton.style.left = this.calculateScaledX(400) + 'px';
        scoreTableButton.style.top = this.calculateScaledY(450) + 'px';
        scoreTableButton.style.fontSize = this.calculateScaledX(35) + 'px';
        scoreTableButton.style.fontSize = this.calculateScaledY(35) + 'px';
        scoreTableButton.style.zIndex = "10";
        scoreTableButton.style.position = 'fixed';

        const createPlayer: HTMLButtonElement = document.createElement('button');
        createPlayer.textContent = 'Create new player';
        createPlayer.id = 'createPlayer';
        createPlayer.style.left = this.calculateScaledX(400) + 'px';
        createPlayer.style.top = this.calculateScaledY(500) + 'px';
        createPlayer.style.fontSize = this.calculateScaledX(35) + 'px';
        createPlayer.style.fontSize = this.calculateScaledY(35) + 'px';
        createPlayer.style.zIndex = "10";
        createPlayer.style.position = 'fixed';
       
        // this.appContainer.append(title);
        this.appContainer.append(this.startButton);
        this.appContainer.append(scoreTableButton);
        this.appContainer.append(createPlayer);
    }

    drawGameOver(): void {
        const title: HTMLHeadingElement = document.createElement('h1');
        title.textContent = 'GAME OVER!';
        title.style.fontFamily = "DotGothic16";
        title.style.left = this.calculateScaledX(450) + 'px';
        title.style.top = this.calculateScaledY(250) + 'px';
        title.style.fontSize = this.calculateScaledX(35) + 'px';
        title.style.fontSize = this.calculateScaledY(35) + 'px';
        title.style.zIndex = "10";
        title.style.color = 'red';
        title.style.position = 'fixed';
        this.appContainer.append(title);
    }

    drawScoreTable(brain: Brain) {

        const title: HTMLHeadingElement = document.createElement('h1');
        title.textContent = 'TOP 10 HIGH SCORES';
        title.style.fontFamily = "DotGothic16";
        title.style.left = this.calculateScaledX(400) + 'px';
        title.style.top = this.calculateScaledY(250) + 'px';
        title.style.fontSize = this.calculateScaledX(35) + 'px';
        title.style.fontSize = this.calculateScaledY(35) + 'px';
        title.style.zIndex = "10";
        title.style.color = 'red';
        title.style.position = 'fixed';

        brain.scoreTable.sort((a, b) => b.getScore - a.getScore);
        const highestScorePlayers: Player[] = brain.scoreTable.filter((player, index) => {
            return index < 10;
        });

        let top: number = 300;
        let position: number = 1;

        highestScorePlayers.forEach(player => {
            if (position < 11) {
                const score: HTMLDivElement = document.createElement('div');
                score.style.fontFamily = "DotGothic16";
                score.style.left = this.calculateScaledX(700) + 'px';
                score.style.top = this.calculateScaledY(top+=25) + 'px';
                score.style.fontSize = this.calculateScaledX(25) + 'px';
                score.style.fontSize = this.calculateScaledY(25) + 'px';
                score.style.zIndex = "10";
                score.style.position = 'fixed';
                score.textContent = player.getScore.toString();
                score.style.color = 'white';

                const name: HTMLDivElement = document.createElement('div');
                name.style.fontFamily = "DotGothic16";
                name.style.left = this.calculateScaledX(400) + 'px';
                name.style.top = this.calculateScaledY(top) + 'px';
                name.style.fontSize = this.calculateScaledX(25) + 'px';
                name.style.fontSize = this.calculateScaledY(25) + 'px';
                name.style.zIndex = "10";
                name.style.position = 'fixed';
                name.textContent = player.getName;
                name.style.color = 'white';

                const place: HTMLDivElement = document.createElement('div');
                place.style.fontFamily = "DotGothic16";
                place.style.left = this.calculateScaledX(380) + 'px';
                place.style.top = this.calculateScaledY(top) + 'px';
                place.style.fontSize = this.calculateScaledX(25) + 'px';
                place.style.fontSize = this.calculateScaledY(25) + 'px';
                place.style.zIndex = "10";
                place.style.position = 'fixed';
                place.textContent = position++ + '.';
                place.style.color = 'white';

                this.appContainer.append(title);
                this.appContainer.append(name);
                this.appContainer.append(score);
                this.appContainer.append(place);
            }
        });
    }


    draw() {

        this.appContainer.innerHTML = '';
        this.setScreenDimensions();

        this.drawBorder();

        if (this.brain.getUserNameEntered) {
            this.drawBrick(this.brain.brick);
            // console.log(this.brain.ball.getLeft);
            // console.log(this.brain.ball.getTop);
            this.drawBall(this.brain.ball);
            // if (!this.brain.bullet.brickCollision) {
            //     this.drawBullet(this.brain.bullet);
            // }
            this.drawPaddle(this.brain.paddle);
            this.drawScore();
            this.drawTurnsLeft();
            this.drawLevel();
            this.drawShootingCountDown();
            this.brain.handleBrickCollisions();
            this.brain.changeLevel();
            this.brain.ballOutOfBounds();
        }
    }
}
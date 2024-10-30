
export class Player {

    constructor(
        private name: string = '',
        private score: number = 0,
        private turns: number = 3,
        private level: number = 1,
        private id: number = 1) {
    }

    public get getName(): string {
        return this.name;
    }
    public set setName(value: string) {
        this.name = value;
    }

    public get getScore(): number {
        return this.score;
    }
    public set setScore(value: number) {
        this.score = value;
    }

    public get getTurns(): number {
        return this.turns;
    }
    public set setTurns(value: number) {
        this.turns = value;
    }

    public get getLevel(): number {
        return this.level;
    }
    public set setLevel(value: number) {
        this.level = value;
    }

    public get getId(): number {
        return this.id;
    }
    public set setId(value: number) {
        this.id = value;
    }
}

export class Paddle {
    private width: number = 200;
    private height: number = 50;
    private intervalId: number | undefined = undefined;

    constructor(private left: number = 0, private top: number = 200, private color: string = 'blue') {
    }

    public get getWidth(): number {
        return this.width;
    }

    public get getHeight(): number {
        return this.height;
    }

    public get getLeft(): number {
        return this.left;
    }

    public set setLeft(value: number) {
        this.left = value;
    }

    public get getTop(): number {
        return this.top;
    }

    public set setTop(value: number) {
        this.top = value;
    }

    public get getColor(): string {
        return this.color;
    }

    public set setColor(value: string) {
        this.color = value;
    }

    validateAndFixPosition(borderThickness: number): void {
        if (this.left < borderThickness) {
            this.left = borderThickness;
            clearInterval(this.intervalId);
            this.intervalId = undefined;
        }

        if ((this.left + this.width) > 1000 - borderThickness) {
            this.left = (1000 - borderThickness) - (this.width);
            clearInterval(this.intervalId);
            this.intervalId = undefined;
        }
    }

    startMove(step: number, borderThickness: number): void {
        if (this.intervalId !== undefined) return;

        this.intervalId = setInterval(() => {
            this.left += step * 35;
            this.validateAndFixPosition(borderThickness);

        }, 40);
    }

    stopMove(borderThickness: number): void {
        if (!this.intervalId) return;
        clearInterval(this.intervalId);
        this.intervalId = undefined;
        this.validateAndFixPosition(borderThickness);
    }
}

export class Brick {
    readonly padding: number = 2;
    readonly offsetTop: number = 30;
    readonly offsetLeft: number = 30;
    readonly brickImageSrc: string = 'img/icons8-pistol-50.png';

    private left: number = 0;
    private top: number = 0;
    private score: number = 1;
    private visible: boolean = true;
    private image: object | undefined = undefined;

    constructor(private width: number = 70, private height: number = 25, private color: string = 'yellow') {
    }

    public get getLeft(): number {
        return this.left;
    }

    public set setLeft(value: number) {
        this.left = value;
    }

    public get getTop(): number {
        return this.top;
    }

    public set setTop(value: number) {
        this.top = value;
    }

    public get getScore(): number {
        return this.score;
    }

    public set setScore(value: number) {
        this.score = value;
    }

    public get getVisible(): boolean {
        return this.visible;
    }

    public set setVisible(value: boolean) {
        this.visible = value;
    }

    public get getImage(): object | undefined {
        return this.image;
    }

    public set setImage(value: object | undefined) {
        this.image = value;
    }

    public get getWidth(): number {
        return this.width;
    }

    public set setWidth(value: number) {
        this.width = value;
    }

    public get getHeight(): number {
        return this.height;
    }

    public set setHeight(value: number) {
        this.height = value;
    }

    public get getColor(): string {
        return this.color;
    }

    public set setColor(value: string) {
        this.color = value;
    }
}

export class Ball {
    readonly width: number = 20;
    readonly height: number = 20;

    private bounceBackHorizontal: string = '';
    private bounceBackVertical: string = '';
    private ballAngle: number = this.left;
    private ballSpeed: number = 6;

    private brickCollision: boolean = false;
    pause: boolean = false;

    private ballIntervalId: number | undefined = undefined;

    constructor(private left: number = 0, private top: number = 300, private color: string = 'blue') {
    }

    public get getLeft(): number {
        return this.left;
    }

    public set setLeft(value: number) {
        this.left = value;
    }

    public get getTop(): number {
        return this.top;
    }

    public set setTop(value: number) {
        this.top = value;
    }

    public get getColor(): string {
        return this.color;
    }

    public set setColor(value: string) {
        this.color = value;
    }

    public get getBounceBackHorizontal(): string {
        return this.bounceBackHorizontal;
    }

    public set setBounceBackHorizontal(value: string) {
        this.bounceBackHorizontal = value;
    }

    public get getBounceBackVertical(): string {
        return this.bounceBackVertical;
    }

    public set setBounceBackVertical(value: string) {
        this.bounceBackVertical = value;
    }

    public get getBallAngle(): number {
        return this.ballAngle;
    }

    public set setBallAngle(value: number) {
        this.ballAngle = value;
    }

    public get getBallSpeed(): number {
        return this.ballSpeed;
    }

    public set setBallSpeed(value: number) {
        this.ballSpeed = value;
    }

    public get getBrickCollision(): boolean {
        return this.brickCollision;
    }

    public set setBrickCollision(value: boolean) {
        this.brickCollision = value;
    }

    toggleballPause(): void {
        this.pause = !this.pause;
        if (this.pause) {
            this.pauseBall();
        }
    }

    validateAndFixPosition(borderThickness: number, paddle: Paddle): void {
        
        if ((this.top <= borderThickness) || this.brickCollision) {      
            if (!this.brickCollision) {
                this.top = borderThickness;
            }      
            this.bounceBackHorizontal = 'down';
            this.bounceBackVertical = '';
            this.ballAngle = (getRandomNumberInRange(-2, 2));
            this.brickCollision = false;
        }
        
        //When ball touches the paddle
        if ((this.top >= 1000 - borderThickness - paddle.getHeight - this.height)
             && (this.left >= paddle.getLeft && this.left <= paddle.getLeft + paddle.getWidth)) {
            this.top = 1000 - borderThickness - paddle.getHeight - this.height;
            this.bounceBackHorizontal = 'up';
            this.bounceBackVertical = '';

            const leftAreaofPaddle: number = paddle.getWidth / 4;
            const rightAreaofPaddle: number = leftAreaofPaddle;
            const centerOfPaddle: number = leftAreaofPaddle * 2;

            if (this.left <= paddle.getLeft + leftAreaofPaddle) {
                this.ballAngle = (getRandomNumberInRange(2, 0.2));
            }

            else if (this.left >= paddle.getLeft + leftAreaofPaddle + centerOfPaddle) {
                this.ballAngle = (getRandomNumberInRange(-2, -0.2));
            }

            else if (this.left >= paddle.getLeft + leftAreaofPaddle && this.left <= paddle.getLeft + rightAreaofPaddle + centerOfPaddle) {
                this.ballAngle = (getRandomNumberInRange(-0.2, 0.2));
            }
        }

        if (this.left >= (1000 - borderThickness - this.width)) {
            this.bounceBackVertical = 'left';
            this.ballAngle = (getRandomNumberInRange(1, 2));
        }

        if (this.left <= borderThickness) {
            this.bounceBackVertical = 'right';
            this.ballAngle = (getRandomNumberInRange(1, 2));
        }

        // console.log(this.top);
    }

    pauseBall(): void {
        clearInterval(this.ballIntervalId);
    }

    ballMove(borderThickness: number, paddle: Paddle): void {

        // console.log("TERETERE2222222222");

        if (this.ballIntervalId !== undefined) return;

        this.ballIntervalId = setInterval(() => {

            // console.log("BALL LEFT:" + this.left);
            // console.log("BALL TOP:" + this.top);
            // console.log(this.ballSpeed);

            if (!this.pause) {
                // console.log("PAUSED" + this.pause)
                // console.log("BALL LEFT:" + this.left);
                // console.log("BALL bounceBackVertical:" + this.bounceBackVertical);
                // console.log("BALL bounceBackHorizontal:" + this.bounceBackHorizontal);
                if (this.bounceBackVertical === '' && this.bounceBackHorizontal === '') {
                    this.top += this.ballSpeed;
                    this.left += this.ballAngle;
                    console.log("A");
                }
                else if (this.bounceBackVertical === 'left' && this.bounceBackHorizontal === 'up') {
                    this.top -= this.ballSpeed;
                    this.left -= this.ballAngle;
                    console.log("B");
                }
                else if (this.bounceBackVertical === 'left' && this.bounceBackHorizontal === 'down') {
                    this.top += this.ballSpeed;
                    this.left -= this.ballAngle;
                    console.log("C");
                }
                else if (this.bounceBackVertical === 'right' && this.bounceBackHorizontal === 'up') {
                    this.top -= this.ballSpeed;
                    this.left += this.ballAngle;
                    console.log("D");
                }
                else if (this.bounceBackVertical === 'right' && this.bounceBackHorizontal === 'down') {
                    this.top += this.ballSpeed;
                    this.left += this.ballAngle;
                    console.log("E");
                }
                else if (this.bounceBackHorizontal === 'up') {
                    this.top -= this.ballSpeed;
                    this.left -= this.ballAngle;
                    console.log("F");
                }
                else if (this.bounceBackHorizontal === 'down') {
                    this.top += this.ballSpeed;
                    this.left += this.ballAngle;
                    console.log("G");
                }

                this.validateAndFixPosition(borderThickness, paddle);
            }
        }, 10);
    }
}

export class Bullet {
    readonly width: number = 10;
    readonly height: number = 30;

    private brickCollision: boolean = false;
    private drawBullet: boolean = false;

    private bulletIntervalId: number | undefined = undefined;

    constructor(private left: number = 0, private top: number = 300, private color: string = 'red') {
    }

    public get getLeft(): number {
        return this.left;
    }

    public set setLeft(value: number) {
        this.left = value;
    }

    public get getTop(): number {
        return this.top;
    }

    public set setTop(value: number) {
        this.top = value;
    }

    public get getColor(): string {
        return this.color;
    }

    public set setColor(value: string) {
        this.color = value;
    }

    public get getBrickCollision(): boolean {
        return this.brickCollision;
    }

    public set setBrickCollision(value: boolean) {
        this.brickCollision = value;
    }

    public get getDrawBullet(): boolean {
        return this.drawBullet;
    }

    public set setDrawBullet(value: boolean) {
        this.drawBullet = value;
    }

    clearBullet(): void {
        clearInterval(this.bulletIntervalId);
    }

    bulletMove(): void {
        this.bulletIntervalId = setInterval(() => {
            this.top -= 16;
            this.validateAndFixPosition();
            
        }, 10);
    }

    validateAndFixPosition(): void {
        
        if (this.brickCollision || this.top < 0) {      
            this.top = 920;
            this.clearBullet();
            this.drawBullet = false;
            this.brickCollision = false;
        }
    }
}

export default class Brain {
    readonly width: number = 1000;
    readonly height: number = 1000;
    readonly borderThickness: number = 30;
    scoreTable: Player[] = [];

    paddle: Paddle = new Paddle(400, this.height - 50 - this.borderThickness, 'navy');
    ball: Ball = new Ball(477, 300, 'white');
    bullet: Bullet = new Bullet(this.paddle.getLeft + (this.paddle.getWidth / 2), this.paddle.getTop, 'red');
    brick: Brick = new Brick(70, 25, 'yellow');
    player: Player = new Player('', 0, 3, 1, this.scoreTable.length === 0 ? 1 : this.scoreTable.length);
    bricks: Brick[] = [];

    private toggleMenu: boolean = false;
    private userNameEntered: boolean = false;
    private gameStarted: boolean = false;
    private gameOver: boolean = false;
    private shootingEnabled: boolean = false;
    private shootingIntervalId: number | undefined = undefined;
    private shootingCountDownValue: number = 20;

    readonly scoreMappings: { [key: string]: number } = {
        'yellow': 1,
        'green': 3,
        'orange': 5,
        'red': 7
    };

    constructor() {
        console.log("Brain ctor");
    }

    public get getToggleMenu(): boolean {
        return this.toggleMenu;
    }
    public set setToggleMenu(value: boolean) {
        this.toggleMenu = value;
    }

    public get getUserNameEntered(): boolean {
        return this.userNameEntered;
    }
    public set setUserName(value: boolean) {
        this.userNameEntered = value;
    }

    public get getGameStarted(): boolean {
        return this.gameStarted;
    }
    public set setGameStarted(value: boolean) {
        this.gameStarted = value;
    }

    public get getGameOver(): boolean {
        return this.gameOver;
    }
    public set setGameOver(value: boolean) {
        this.gameOver = value;
    }

    public get getShootingEnabled(): boolean {
        return this.shootingEnabled;
    }
    public set setShootingEnabled(value: boolean) {
        this.shootingEnabled = value;
    }

    public get getShootingIntervalId(): number | undefined {
        return this.shootingIntervalId;
    }
    public set setShootingIntervalId(value: number | undefined) {
        this.shootingIntervalId = value;
    }

    public get getShootingCountDownValue(): number {
        return this.shootingCountDownValue;
    }
    public set setShootingCountDownValue(value: number) {
        this.shootingCountDownValue = value;
    }

    startMovePaddle(paddle: Paddle, step: number): void {
        paddle.startMove(step, this.borderThickness);
    }

    stopMovePaddle(paddle: Paddle): void {
        paddle.stopMove(this.borderThickness);
    }

    movingBall(): void {
        this.ball.ballMove(this.borderThickness, this.paddle);

    }

    shootingBullet(): void {
        this.bullet.bulletMove();

    }

    createPlayer(input: string): void {
        this.player = new Player(input.valueOf(), 0, 3, 1, this.scoreTable.length === 0 ? 1 : this.scoreTable.length + 1);
        this.scoreTable.push(this.player);
        this.userNameEntered = true;
        this.toggleMenu = true;
    }

    startGame(): void {
        console.log('Game started!');
        this.toggleMenu = false;
        this.ball.pause = false;
        this.paddle = new Paddle(400, this.height - 50 - this.borderThickness, 'navy');
        this.ball = new Ball(477, 300, 'white');
        this.brick = new Brick(70, 25, 'yellow');
        this.player = new Player('player', 0, 3, 1, this.scoreTable === undefined ? 1 : this.scoreTable.length);
        this.bricks = [];
        this.addBricksToList();
        this.shootingCountDownValue = 20;
    }
    
    showScoreTable(): void {
        console.log('Showing scoretable...');
    }

    toggleMenuVisible(): void {
        this.toggleMenu = !this.toggleMenu;
    }

    updatePlayerData(score: number): void {
        this.scoreTable.forEach(player => {
            if (player.getId === this.player.getId) {
                if (player.getScore < this.player.getScore) {
                    player.setScore = score;
                }
                if (player.getLevel < this.player.getLevel) {
                    player.setLevel = this.player.getLevel;
                }
            }
        })
    }

    ballOutOfBounds(): void {
        if (this.ball.getTop > 1000) {
            if (this.player.getTurns > 1) {
                this.player.setTurns = this.player.getTurns - 1;
                const speed = this.ball.getBallSpeed;
                this.ball = new Ball(477, 300, 'white');
                this.ball.setBallSpeed = speed;
                this.movingBall();
            } else {
                this.player.setTurns = this.player.getTurns - 1;
                this.ball = new Ball(477, 300, 'white');
                this.gameOver = true;
                console.log("Game Over!");
            }
        }
    }

    shootingCountdown(): void {
        this.shootingIntervalId = setInterval(() => {
            this.shootingCountDownValue--;

            if (this.shootingCountDownValue <= 0) {
                this.shootingEnabled = false;
                this.shootingCountDownValue = 20;
                clearInterval(this.shootingIntervalId);
                return;
              }
        }, 1000);
    }

    handleBrickCollisions(): void {
        for (let i = 0; i < this.bricks.length; i++) {
            const brick = this.bricks[i];
            const collision = this.checkCollision(this.ball, brick, this.bullet);

            if (brick.getVisible && collision != 'noCollision') {
                if (brick.getImage != undefined) {
                    this.shootingEnabled = true;
                    this.shootingCountdown();
                }
                if (!this.gameOver) {
                    this.player.setScore = this.player.getScore + this.scoreMappings[brick.getColor];
                }
                this.updatePlayerData(this.player.getScore);
                if (collision === 'ballCollision') {
                    this.ball.setBrickCollision = true;
                }
                if (collision === 'bulletCollision') {
                    this.bullet.setBrickCollision = true;
                    this.bullet.setDrawBullet = false;
                }
                this.removeBrick(brick);
                break;
            }
        }
    }

    changeLevel(): void {
        // if (this.bricks.length === 0) {
        //     this.paddle = new Paddle(400, this.height - 50 - this.borderThickness, 'navy');
        //     const speed = this.ball.getBallSpeed + 3;
        //     this.ball = new Ball(477, 300, 'white');
        //     this.brick = new Brick(70, 25, 'yellow');
        //     this.bricks = [];
        //     this.addBricksToList();
        //     this.player.setTurns = 3;
        //     this.player.setLevel = this.player.getLevel + 1;
        //     this.ball.setBallSpeed = speed;
        //     this.movingBall();
        // }
    }

    checkCollision(ball: Ball, brick: Brick, bullet: Bullet): string {

        const bulletBottom: number = bullet.getTop + bullet.height;
        const bulletRight: number = bullet.getLeft + bullet.width;
        const ballRight: number = ball.getLeft + ball.width;
        const ballBottom: number = ball.getTop + ball.height;
        const brickRight: number = brick.getLeft + brick.getWidth;
        const brickBottom: number = brick.getTop + brick.getHeight;
    
        if (ballRight > brick.getLeft &&
            ball.getLeft < brickRight &&
            ballBottom > brick.getTop &&
            ball.getTop < brickBottom) {
                return 'ballCollision';
        }
        else if (bulletRight > brick.getLeft &&
                 bullet.getLeft < brickRight &&
               bulletBottom > brick.getTop &&
              bullet.getTop < brickBottom) {
            return 'bulletCollision';
        } else {
            return 'noCollision';
        }
    }

    removeBrick(brick: Brick): void {
        this.bricks = this.bricks.filter(b => b !== brick);
    }

    addBricksToList(): void {

        const rows: number = 8;
        const cols: number = 10;
    
        const brickRowColors: string[] = ['red', 'red', 'orange', 'orange', 'green', 'green', 'yellow', 'yellow'];
    
        const totalWidth: number = (this.brick.getWidth * cols) + (this.brick.padding * (cols - 1));
        const startX: number = ((this.width) - totalWidth) / 2;
        
        const specialBrickRow: number = getRandomNumberInRange(0, rows);
        const specialBrickCol: number = getRandomNumberInRange(0, cols);
    
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {

                const brick: Brick = new Brick();

                brick.setLeft = startX + (col * (this.brick.getWidth + this.brick.padding));
                brick.setTop = (row * (this.brick.getHeight + this.brick.padding)) + this.borderThickness;
                brick.setWidth = this.brick.getWidth;
                brick.setHeight = this.brick.getHeight;
                brick.setColor = brickRowColors[row];
                brick.setScore = this.brick.getScore;
                // brick.setVisible = true;
                
                if (row === 7 && col === 2) {
                        
                    brick.setImage = {
                        src: this.brick.brickImageSrc,
                        width: this.brick.getWidth, 
                        height: this.brick.getHeight,
                        title: "shooting",
                        id: "shooting"
                    }
                };
                    console.log(brick.getImage);
    
                this.bricks.push(brick);
            }
        }
    }
}

function getRandomNumberInRange(min: number, max: number) {
    return Math.random() * (max - min) + min;
  }
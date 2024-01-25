
using DAL;
using Domain;
using GameUtilities;
using UnoEngine;
using static System.Console;

namespace ConsoleUI;

public class GameController(GameEngine engine, IGameRepository repository)
{
    private ValidateInputs Validate { get; set; } = new();
    private GameState State => engine.State;

    public static void Main(string[] args)
    {
        
    }

    public void Run(string? messages = null)
    {
        while (true)
        {
            WriteLine(messages ?? "");
            WriteLine("THE GAME HAS BEGUN!");
            
            HandlePlayerTurns();
            Clear();

            if (State.ExitGame)
            {
                break;
            }

            if (State.GameRounds.Count >= State.Rules.GameRoundsAmount
                || State.Players.Any(x => x.Score >= State.Rules.PointsToWin))
            {
                Clear();
                State.GameOver = true;
                ForegroundColor = ConsoleColor.White;
                WriteLine();
                WriteLine();
                WriteLine();
                Utilities.PrintStringWithDelay("---------------------------G A M E  O V E R!" +
                                               "---------------------------", 40);
                WriteLine();
                Utilities.PrintStringWithDelay($"                      {State.Winner!.NickName}" +
                                               $"  i s  t h e  w i n n e r!", 40);
                
                Thread.Sleep(5000);
                break;
            }
            
            if (!State.Players.Any(x => x.Score >= State.Rules.PointsToWin))
            {
                engine.ResetGameState();
                engine.InitializeGame();
                WriteLine($"ROUND {State.GameRounds.Count + 1} HAS BEGUN!");
            }
        }
    }
    
    private void HandlePlayerTurns()
    {
        PlayerTurn? previousTurn = State.PlayerTurns.Count > 1 ? State.PlayerTurns.Peek() : null;

        while (true)
        {
            State.CurrentPlayer = State.Players[State.PlayerIndex];
            var firstTurnResult = engine.HandleFirstTurn();

            if (firstTurnResult.ShouldPlayMatchingCard)
            {
                var playMatchingCard = engine.PlayMatchingCard(State.CurrentPlayCardOnTheTable!);
                if (playMatchingCard.PlayCard)
                {
                    var playCardResult = engine.PlayCard(State.CurrentPlayer, State.CurrentPlayCardOnTheTable!);
                    previousTurn = playCardResult.PlayerTurn!;
            
                    if (playCardResult.ShouldDeclareColor)
                    {
                        var beforeValidation = engine.DeclareColorBeforeValidation(playCardResult.PlayerTurn!);
            
                        if (beforeValidation.PromptPlayerTurn)
                        {
                            WriteLine(string.Empty);
                            WriteLine($"Player {State.CurrentPlayer!.NickName} it is your turn!");
                            WriteLine(string.Empty);
                        }

                        if (State.CurrentPlayer.PlayerType != EPlayerType.AI)
                        {
                            int counter = 1;
                            foreach (var color in beforeValidation.CardColors!)
                            {
                                WriteLine($"{counter++}) {color}");
                            }
                            
                            var declareColorResult = engine.DeclareColor(playCardResult.PlayerTurn!);
                            previousTurn.DeclaredColor = declareColorResult.PlayerTurn!.DeclaredColor;
                        }
                        else
                        {
                            previousTurn.DeclaredColor = playCardResult.PlayerTurn!.DeclaredColor;
                        }
                    }
            
                    if (playCardResult.ShouldSwapHandsWithAnotherPlayer)
                    {
                        int counter = 1;
                        State.Players.ForEach(x => WriteLine($"{counter++}) {x.NickName}"));
            
                        GameEngineResults.HandleSwapHandsWithAnotherPlayerResult swapResult;
                        do
                        {
                            swapResult = engine.SwapHandsWithAnotherPlayer(State.CurrentPlayer);
                            if (swapResult.CannotChooseSelf)
                            {
                                WriteLine("You cannot choose yourself. Please choose different player.");
                            }
                            
                        } while (swapResult.CannotChooseSelf);
                        
                        WriteLine($"You swapped hands with {swapResult.SwappedWithPlayer!.NickName}!");
                    }
            
                    if (playCardResult.ShouldSwapAllHands)
                    {
                        engine.SwapAllHands(State.DirectionOfPlay);
                        WriteLine("All the players swapped their cards!");
                    }
                }
            }
            
            if (engine.IsPlayerAttacked(previousTurn!))
            {
                var attackResult = engine.HandlePlayerAttack(previousTurn!,
                    State.CurrentPlayer, previousTurn!.DeclaredColor);

                if (attackResult.ShouldPromptForStacking)
                {
                    if (State.CurrentPlayer.PlayerType == EPlayerType.Human)
                    {
                        WriteLine($"{attackResult.Player!.NickName}," +
                                          $" now you can draw {engine.GetDrawCount(previousTurn)} cards" +
                                          $" or play another {previousTurn.Result} card!");
                        WriteLine("d) Draw cards");
                        WriteLine("s) Stack another card");
                    }
                    
                    engine.PromptForStacking(previousTurn, State.CurrentPlayer.PlayerType == EPlayerType.AI ? "s" : null);
                }
                else
                {
                    var handleAttackResult = engine.HandleAttackByPreviousPlayer(previousTurn.Card!,
                        attackResult.Player!, previousTurn.DeclaredColor);
                    
                    if (handleAttackResult.ShouldHandleSkipCard)
                    {
                        WriteLine($"Player {attackResult.Player!.NickName} was skipped!");
                    }
                    if (handleAttackResult.ShouldHandleDrawTwoCard)
                    {
                        engine.HandleDrawTwoCard(attackResult.Player!, handleAttackResult.PreviousTurn!,
                                                                          handleAttackResult.StackCount);
                        WriteLine($"Player {attackResult.Player!.NickName}" +
                                          $" drew {handleAttackResult.StackCount * 2} cards!");
                    }
                    if (handleAttackResult.ShouldHandleDrawFourCard)
                    {
                        WriteLine("Previous player played Draw Four card!");
                        if (State.CurrentPlayer.PlayerType == EPlayerType.Human)
                        {
                            WriteLine("Press 'c' to challenge previous player or 'Enter' to continue");
                        }
                        
                        var handleDrawFourResult = engine.HandleDrawFourCard(attackResult.Player!,
                            handleAttackResult.PreviousTurn!, handleAttackResult.StackCount);
                        
                        if (handleDrawFourResult.ShouldHandleChallenge)
                        {
                            var handleChallengeResult = engine.HandleChallenge(attackResult.Player!,
                                handleAttackResult.PreviousTurn!, handleDrawFourResult.PreviousPlayer);
                            if (handleChallengeResult.DidCheat)
                            {
                                WriteLine();
                                WriteLine($"LAST PLAY CARD ON THE TABLE WAS:" +
                                                  $" {handleChallengeResult.PenultimateCard!.CardValue}" +
                                                  $" {handleChallengeResult.PenultimateCard!.CardColor}");
                                WriteLine();
                                WriteLine($"Previous player {handleDrawFourResult.PreviousPlayer!.NickName}" +
                                                  $" had these cards:");
                                handleDrawFourResult.PreviousPlayer!.Hand!.ForEach(x => 
                                WriteLine($"{x.CardValue}, {x.CardColor}"));
                                WriteLine($"{handleDrawFourResult.PreviousPlayer?.NickName}" +
                                                  $" cheated and draws 4 cards!");
                            }
                            else
                            {
                                WriteLine($"{handleDrawFourResult.PreviousPlayer!.NickName} did not cheat!");
                                WriteLine($"Player {attackResult.Player!.NickName} who challenged" +
                                                  $" {handleDrawFourResult.PreviousPlayer!.NickName} will draw six cards!");
                            }
                        }
                        if (handleDrawFourResult.ShouldDrawCards)
                        {
                            engine.TakeDrawFourCards(attackResult.Player!, handleDrawFourResult.StackCount);
                            WriteLine($"Player {attackResult.Player!.NickName}" +
                                              $" will draw {handleDrawFourResult.StackCount * 4} cards!");
                        }
                    }
                    
                    previousTurn = handleAttackResult.PreviousTurn;
                }
                if (State.SwitchToNextPlayer)
                {
                    engine.ChangePlayerIndex();
                }
            }
            
            // Console.WriteLine(previousTurn!.Result.ToString());
            
            var directionOfPlay = engine.HandlePlayDirection(previousTurn);
            
            if (directionOfPlay)
            {
                WriteLine("Direction of play is now "
                                  + (State.DirectionOfPlay == DirectionOfPlay.CounterClockwise
                                  ? "counter-clockwise" : "clockwise"));
            }

            if (engine.ShoutedUno(previousTurn))
            {
                WriteLine($"{previousTurn!.Player!.NickName} SHOUTED UNO!");
            }

            if (engine.IsRoundOver())
            {
                var declareWinnerResult = engine.DeclareWinnerIfNoMoreCardsLeft();
                
                WriteLine("No cards left in the draw pile. Cannot reshuffle any cards.");
                WriteLine($"Round {State.GameRounds.Count + 1} is over");
                foreach (var player in State.Players)
                {
                    WriteLine($"{player.NickName} has {player.Hand!.Sum(x => x.Score)}" +
                                      $" points in his hand.");
                }

                WriteLine($"Winner {declareWinnerResult.WinningPlayer!.NickName}" +
                                  $" gets {declareWinnerResult.Score} points!");

                Thread.Sleep(7000);
                
                break;
            }

            // Console.WriteLine($"\nPlayer {State.CurrentPlayer!.NickName} it is your turn!");
            
            var selectedCardByPlayer = State.CurrentPlayCardOnTheTable;
            
            ForegroundColor = ConsoleColor.Green;
            WriteLine($"\n{State.CurrentPlayer!.NickName}, it is your turn!");

            if (State.Players.Any(x => x.PlayerType == EPlayerType.Human))
            {
                Validate.ValidateAndPromptInput("Press 'ENTER' to continue", null,
                    canBeEmptyString: true, inputMode: ValidateInputs.InputMode.Any);
            }
            ForegroundColor = ConsoleColor.White;
            
            var playerShoutedUno = engine.HandleIfLastPlayerShoutedUno(previousTurn!);

            if (playerShoutedUno.ShouldDrawCards)
            {
                WriteLine($"{previousTurn!.Player!.NickName} didn't shout Uno!");
                WriteLine($"{previousTurn.Player!.NickName} will draw two cards!");
            }
            
            DisplayCurrentGameState(previousTurn!.DeclaredColor);
            if (State.Players.Any(x => x.PlayerType == EPlayerType.Human)
                && State.CurrentPlayer.PlayerType == EPlayerType.Human)
            {
                DisplayPlayerHand(State.CurrentPlayer);
            }
            
            GameEngineResults.PlayerChooseCardResult playerChooseCardResult;
            GameEngineResults.PlayMatchingCardResult playMatchingCardResult;
            
            repository.Save(State.Id, State);
            
            do
            {
                playerChooseCardResult = State.CurrentPlayer.PlayerType == EPlayerType.Human
                    ? engine.HumanChooseCard(State.CurrentPlayer, previousTurn.DeclaredColor)
                    : engine.AiChooseCard(State.CurrentPlayer, previousTurn.DeclaredColor);
                
                if (playerChooseCardResult.ShouldExitOrDraw)
                {

                    var exitOrDrawResult = engine.HandleExitOrDraw(playerChooseCardResult.ValidationResult,
                        State.CurrentPlayer, previousTurn.DeclaredColor);
                    if (exitOrDrawResult.ExitGame)
                    {
                        WriteLine("Exit Game");
                    }

                    if (exitOrDrawResult.DrawCard)
                    {
                        var drawCardResult = engine.DrawCard(State.CurrentPlayer, previousTurn.DeclaredColor);

                        if (drawCardResult.IsOutOfCards)
                        {
                            WriteLine("Out of cards!");
                        }
                        else
                        {
                            WriteLine($"Drawn card is: {drawCardResult.DrawnCard!.CardValue}," +
                                              $" {drawCardResult.DrawnCard!.CardColor}");
                        }

                        if (drawCardResult.CannotPlayDrawnCard)
                        {
                            WriteLine("You cannot play this card. It will be next player's turn.");
                        }
                    
                        GameCard? selectedCard = engine.CheckIfForceDrawPlay(drawCardResult.PlayerTurn!);
                        selectedCardByPlayer = selectedCard;
                    }
                }
                else
                {
                    selectedCardByPlayer = playerChooseCardResult.SelectedCard;
                }
                
                playMatchingCardResult = engine.PlayMatchingCard(selectedCardByPlayer, previousTurn.DeclaredColor);
                
                if (playerChooseCardResult.ShouldExitOrDraw)
                {
                    break;
                }
                
                // if (playerChooseCardResult.IsValidCardSelection)
                // {
                //     selectedCardByPlayer = playerChooseCardResult.SelectedCard;
                // }
                
                if (!playMatchingCardResult.IsCardPlayable && State.CurrentPlayer.PlayerType != EPlayerType.AI)
                {
                    WriteLine("This card cannot be played!");
                }
                if (playerChooseCardResult.CardValidation.StackCardsNotValid)
                {
                    WriteLine($"You can play only {previousTurn.Result} card!");
                }
                if (playerChooseCardResult.CardValidation.IsValid && playMatchingCardResult.IsCardPlayable)
                {
                    WriteLine($"{State.CurrentPlayer.NickName} selected card: {playerChooseCardResult.SelectedCard!.CardValue}," +
                                      $" {playerChooseCardResult.SelectedCard!.CardColor}");
                }
                if (playerChooseCardResult.CardValidation.DeclaredColorNotValid)
                {
                    WriteLine($"You can play only {previousTurn.DeclaredColor} cards");
                }
                if (!playerChooseCardResult.CardValidation.StackCardsNotValid
                    && playMatchingCardResult.PlayNoMatchingCard
                    && !playerChooseCardResult.CardValidation.DeclaredColorNotValid)
                {
                    previousTurn = playMatchingCardResult.PlayerTurn;
                    break;
                }
                
            } while (playerChooseCardResult.ShouldPlayerChooseCard
                     || !playMatchingCardResult.IsCardPlayable
                     || playerChooseCardResult.CardValidation.StackCardsNotValid
                     || playerChooseCardResult.CardValidation.DeclaredColorNotValid);  
              
            if (State.ExitGame)
            {
                break;
            }
            
            if (playMatchingCardResult.PlayCard)
            {
                var playCardResult = engine.PlayCard(State.CurrentPlayer, selectedCardByPlayer!);
                
                previousTurn = playCardResult.PlayerTurn;

                if (playCardResult.ShouldDeclareColor)
                {
                    var beforeValidation = engine.DeclareColorBeforeValidation(playCardResult.PlayerTurn!);

                    if (State.CurrentPlayer.PlayerType == EPlayerType.Human)
                    {
                        WriteLine();
                        WriteLine($"Player {State.CurrentPlayer!.NickName} it is your turn!");
                        WriteLine();
                    }
                    
                    if (State.CurrentPlayer.PlayerType != EPlayerType.AI)
                    {
                        int counter = 1;
                        foreach (var color in beforeValidation.CardColors!)
                        {
                            WriteLine($"{counter++}) {color}");
                        }
                            
                        var declareColorResult = engine.DeclareColor(playCardResult.PlayerTurn!);
                        previousTurn!.DeclaredColor = declareColorResult.PlayerTurn!.DeclaredColor;
                    }
                    else
                    {
                        previousTurn!.DeclaredColor = engine.AiColorDeclaration(State.CurrentPlayer);
                        // previousTurn!.DeclaredColor = ECardColor.Green;
                    }
                }

                if (playCardResult.ShouldSwapHandsWithAnotherPlayer)
                {
                    int counter = 1;
                    State.Players.ForEach(x => WriteLine($"{counter++}) {x.NickName}"));

                    GameEngineResults.HandleSwapHandsWithAnotherPlayerResult swapResult;
                    do
                    {
                        swapResult = engine.SwapHandsWithAnotherPlayer(State.CurrentPlayer);
                        if (swapResult.CannotChooseSelf)
                        {
                            WriteLine("You cannot choose yourself. Please choose different player.");
                        }
                        
                    } while (swapResult.CannotChooseSelf);
                    
                    WriteLine($"You swapped hands with {swapResult.SwappedWithPlayer!.NickName}!");
                }

                if (playCardResult.ShouldSwapAllHands)
                {
                    engine.SwapAllHands(State.DirectionOfPlay);
                    WriteLine("All the players swapped their cards!");
                }
            }

            if (State.CurrentPlayer.PlayerType == EPlayerType.AI)
            {
                // Thread.Sleep(3000);
            }
            
            engine.HandleUnoShout(previousTurn!);
            if (previousTurn!.DidShoutUno)
            {
                WriteLine($"{State.CurrentPlayer!.NickName} SHOUTED UNO!");
            }
            if (previousTurn.Result != TurnResult.Reversed)
            {
                State.PlayerIndex = engine.NextPlayerIndex(State.PlayerIndex);
            }

            var winner = engine.DeclareWinner();
            if (winner != null)
            {
                WriteLine($"Player {winner.NickName} wins!");

                WriteLine($"Winner {winner.NickName} gets" +
                                  $" {State.Players.Sum(player => player.Hand!.Sum(card => card.Score))} points!");
                
                State.Players.ForEach(player => WriteLine($"{player.NickName} has " +
                                                                  $"{player.Hand!.Sum(x => x.Score)}" +
                                                                  $" points in his hand."));
                
                WriteLine();
                
                foreach (var player in State.Players)
                {
                    WriteLine($"{player.NickName} total points: {player.Score}");
                }
                
                Thread.Sleep(1000);
            }
            repository.Save(State.Id, State);

            if (State.RoundOver)
            {
                break;
            }

            WriteLine("Game saved.");
            WriteLine();
            engine.ContinueOrExitGame();
            Clear();
        }
    }
    
    private void DisplayCurrentGameState(ECardColor? declaredColor)
    {
        ForegroundColor = ConsoleColor.Green;
        WriteLine($"\nCURRENT PLAY CARD ON THE TABLE:" +
                          $" {State.CurrentPlayCardOnTheTable!.CardValue}," +
                          $" {State.CurrentPlayCardOnTheTable!.CardColor}\n");
        ForegroundColor = ConsoleColor.White;
        
        if (!State.RoundOver)
        {
            State.Players.ForEach(pl => WriteLine($"{pl.NickName}'s card count: {pl.Hand!.Count}"));
        }
        
        ForegroundColor = ConsoleColor.DarkCyan;
        WriteLine($"Direction of play is:" +
                          $" {(State.DirectionOfPlay == DirectionOfPlay.CounterClockwise
                              ? "Counter-Clockwise"
                              : "Clockwise")}");
        ForegroundColor = ConsoleColor.White;
        
        if (State.PlayerTurns.Count > 1)
        {
            WriteLine($"Last player: {State.PlayerTurns.Peek().Player!.NickName}");
            WriteLine($"Last player's card count: {State.PlayerTurns.Peek().Player!.Hand!.Count}");
        }
        ForegroundColor = ConsoleColor.DarkYellow;
        WriteLine($"Current player: {State.CurrentPlayer!.NickName}");
        WriteLine($"Amount of cards in draw pile: {State.DrawPile.Count}");
        WriteLine($"Player type: {State.CurrentPlayer.PlayerType}");
        ForegroundColor = ConsoleColor.White;
        WriteLine();

        if (declaredColor != null)
        {
            ForegroundColor = ConsoleColor.DarkMagenta;
            WriteLine($"Declared color is: {declaredColor}\n");
            ForegroundColor = ConsoleColor.White;
        }
    }
    
    private void DisplayPlayerHand(Player player)
    {
        WriteLine("Pick a card from your hand:");
        int counter = 1;
        ForegroundColor = ConsoleColor.Cyan;
        player.Hand!.ForEach(x => WriteLine($"{counter++}) {x.CardValue}, {x.CardColor}"));
        ForegroundColor = ConsoleColor.White;
        if (State.PlayerTurns.Any() && !State.PlayerTurns.Peek().StackCards)
        {
            WriteLine("\nOr take a new card from the draw pile:");
            WriteLine("d) Draw card");
            WriteLine("x) Exit to main menu");
        }
    }
}
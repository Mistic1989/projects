
using System.Text;
using Domain;
using GameUtilities;

namespace UnoEngine;

public class GameEngine
{
    public GameState State { get; set; }
    
    private ValidateInputs Validate { get; set; }
    
    public GameEngine()
    {
        State = new GameState();
        Validate = new ValidateInputs();
    }
    
    public string InitializeGame()
    {
        StringBuilder message = new StringBuilder();

        message.AppendLine(InitializeDeck(State.Rules));
        message.AppendLine(ShuffleCards());
        message.AppendLine(DetermineDealer());
        message.AppendLine(ClearAllPlayerHands());
        message.AppendLine(ShuffleCards());
        message.AppendLine(DealCards(State.Rules));
        message.AppendLine(FlipCard());
        message.AppendLine(SetPlayDirection());

        return message.ToString();
    }
    
    public int PreviousPlayerIndex(int i, int movePositionBy = 0)
    {
        if (State.DirectionOfPlay == DirectionOfPlay.Clockwise)
        {
            if (movePositionBy == 0)
            {
                i--;
            }

            i -= movePositionBy;
            if (i < 0)
            {
                i = State.Players.Count - 1;
            }
        }
        else
        {
            if (movePositionBy == 0)
            {
                i++;
            }

            i += movePositionBy;
            if (i >= State.Players.Count)
            {
                i = 0;
            }
        }

        return i;
    }

    public int NextPlayerIndex(int i, int movePositionBy = 0)
    {
        if (State.DirectionOfPlay == DirectionOfPlay.Clockwise)
        {
            if (movePositionBy == 0)
            {
                i++;
            }
            
            i += movePositionBy;
            if (i >= State.Players.Count) //Reset player counter
            {
                i = 0;
            }
        }
        else
        {
            if (movePositionBy == 0)
            {
                i--;
            }
            
            i += movePositionBy;
            if (i < 0)
            {
                i = State.Players.Count - 1;
            }
        }

        return i;
    }
    
    public bool ShoutedUno(PlayerTurn? previousTurn)
    {
        if (previousTurn != null)
        {
            return previousTurn.DidShoutUno;
        }

        return false;
    }
    
    public bool HandlePlayDirection(PlayerTurn? previousTurn)
    {
        if (previousTurn != null && previousTurn.Result == TurnResult.Reversed && State.PlayerTurns.Count > 1)
        {
            ReversePlayDirection();
            return true;
        }
        return false;
    }

    public GameEngineResults.HandlePlayerAttackResult HandlePlayerAttack(PlayerTurn previousTurn, Player player, ECardColor? declaredColor)
    {
        GameEngineResults.HandlePlayerAttackResult result = new GameEngineResults.HandlePlayerAttackResult();

        if (State.Rules.IsHouseRuleActive(EHouseRules.Stacking) && CanPlayerStack(previousTurn, player))
        {
            result.ShouldPromptForStacking = true;
        }
        else
        {
            result.ShouldHandleAttackByPreviousPlayer = true;
        }

        if (previousTurn.Result == TurnResult.Attacked || !previousTurn.ChallengedSuccessfully)
        {
            State.SwitchToNextPlayer = true;
        }
        if (previousTurn.StackCards && State.SwitchToNextPlayer)
        {
            previousTurn.StackCards = false;
        }

        result.Player = player;
        result.PreviousTurn = previousTurn;

        return result;
    }

    public void ChangePlayerIndex()
    {
        State.PlayerIndex = NextPlayerIndex(State.PlayerIndex);
        State.CurrentPlayer = State.Players[State.PlayerIndex];
    }

    public bool IsPlayerAttacked(PlayerTurn previousTurn)
    {
        return previousTurn.Result == TurnResult.Skip
            || previousTurn.Result == TurnResult.DrawTwo
            || previousTurn.Result == TurnResult.WildDrawFour;
    }

    private bool CanPlayerStack(PlayerTurn previousTurn, Player player)
    {
        return (previousTurn.Result == TurnResult.DrawTwo
                && player.Hand!.Any(x => x.CardValue == ECardValue.DrawTwo))
            || (previousTurn.Result == TurnResult.WildDrawFour
                && player.Hand!.Any(x => x.CardValue == ECardValue.DrawFour));
    }

    public void PromptForStacking(PlayerTurn previousTurn, string? userInput = null)
    {
        ValidateInputs.ValidationResult result = Validate.ValidateAndPromptInput(null,
            new List<string> {"d", "s"}, inputMode: ValidateInputs.InputMode.LetterOnly, userInput: userInput);

        if (result.IsValid && result.InputLetter == "s")
        {
            previousTurn.StackCards = true;
            State.SwitchToNextPlayer = false;
        }
    }

    public int GetDrawCount(PlayerTurn previousTurn)
    {
        return previousTurn.Result == TurnResult.DrawTwo ? 2 : 4;
    }

    public void ReversePlayDirection()
    {
        State.DirectionOfPlay = State.DirectionOfPlay == DirectionOfPlay.Clockwise
            ? DirectionOfPlay.CounterClockwise
            : DirectionOfPlay.Clockwise;

        State.PlayerIndex = NextPlayerIndex(State.PlayerIndex, 
                 State.DirectionOfPlay == DirectionOfPlay.Clockwise ? 1 : -1);
        State.CurrentPlayer = State.Players[State.PlayerIndex];
    }

    public GameEngineResults.HandleAttackByPreviousPlayerResult HandleAttackByPreviousPlayer(
        GameCard attackCard, Player player, ECardColor? declaredColor = null)
    {
        GameEngineResults.HandleAttackByPreviousPlayerResult result = 
        new GameEngineResults.HandleAttackByPreviousPlayerResult();
        
        PlayerTurn turn = new PlayerTurn
        {
            Result = TurnResult.Attacked,
            Card = attackCard,
            Player = player,
            DeclaredColor = declaredColor
        };

        switch (attackCard.CardValue)
        {
            case ECardValue.Skip:
                result.ShouldHandleSkipCard = true;
                break;
            case ECardValue.DrawTwo:
                result.ShouldHandleDrawTwoCard = true;
                break;
            case ECardValue.DrawFour:
                result.ShouldHandleDrawFourCard = true;
                break;
        }

        result.Player = player;
        result.PreviousTurn = turn;
        result.StackCount = State.PlayerTurns.Peek().StackCount;

        return result;
    }

    public void HandleDrawTwoCard(Player player, PlayerTurn turn, int stackCount)
    {
        // player.Hand!.AddRange(Draw(stackCount * 2));
        State.Players.FirstOrDefault(x => x.Id == player.Id)!.Hand!.AddRange(Draw(stackCount * 2));
        turn.StackCards = false;
    }
    
    public void TakeDrawFourCards(Player player, int stackCount)
    {
        // player.Hand!.AddRange(Draw(stackCount * 4));
        State.Players.FirstOrDefault(x => x.Id == player.Id)!.Hand!.AddRange(Draw(stackCount * 4));
    }

    public GameEngineResults.HandleDrawFourCardResult HandleDrawFourCard(Player player, PlayerTurn turn,
                                                               int stackCount, string? userInput = null)
    {
        var result = new GameEngineResults.HandleDrawFourCardResult();
        ValidateInputs.ValidationResult validationResult = new ValidateInputs.ValidationResult();

        if (player.PlayerType == EPlayerType.Human)
        {
            validationResult = Validate.ValidateAndPromptInput(
                null, validLetters: new List<string> { "c" }, canBeEmptyString: true,
                inputMode: ValidateInputs.InputMode.LetterOnly, userInput: userInput);
        }
        
        result.PreviousPlayer = State.PlayerTurns.Peek().Player;

        if (validationResult.IsValid && validationResult.InputLetter != null && validationResult.InputLetter == "c")
        {
            result.ShouldHandleChallenge = true;
        }
        else
        {
            result.ShouldDrawCards = true;
            turn.StackCards = false;
        }
        
        result.PlayerTurn = turn;
        result.ValidationResult = validationResult;
        result.StackCount = stackCount;
        
        return result;
    }

    public GameEngineResults.HandleChallengeResult HandleChallenge(Player player, PlayerTurn turn, Player? previousPlayer)
    {
        var result = new GameEngineResults.HandleChallengeResult();
        
        if (State.PlayerTurns.Peek().DidCheat)
        {
            if (State.DiscardPile.Count > 1)
            {
                result.PenultimateCard = State.DiscardPile[^2];
            }

            // previousPlayer?.Hand!.AddRange(Draw(4));
            State.Players.FirstOrDefault(x => x.Id == previousPlayer!.Id)!.Hand!.AddRange(Draw(4));
            turn.ChallengedSuccessfully = true;
            result.DidCheat = true;
        }
        else
        {
            State.Players.FirstOrDefault(x => x.Id == player.Id)!.Hand!.AddRange(Draw(6));
            // player.Hand!.AddRange(Draw(6));
            result.DidCheat = false;
        }
        
        result.WasChallengeSuccessful = turn.ChallengedSuccessfully;
        result.PlayerTurn = turn;
        
        return result;
    }
    
    public GameEngineResults.PlayerChooseCardResult HumanChooseCard(Player player, ECardColor? declaredColor,
                                                                    string? userInput = null)
    {
        var result = new GameEngineResults.PlayerChooseCardResult();
        
        var validation = Validate.ValidateAndPromptInput(
            null, new List<string> { "d", "x" },
            minRange: 1, maxRange: player.Hand!.Count, userInput: userInput);

        result.ValidationResult = validation;

        if (validation.InputLetter == "x" || validation.InputLetter == "d" && validation.IsValid)
        {
            result.ShouldExitOrDraw = true;
            return result;
        }

        if (validation.IsValid && validation.InputNumber != null)
        {
            var selectedCard = player.Hand[validation.InputNumber.Value - 1];
            var validationResult = IsValidCardSelection(selectedCard, declaredColor);
            if (validationResult.IsValid)
            {
                result.CardValidation = validationResult;
                result.IsValidCardSelection = true;
                result.SelectedCard = selectedCard;
                return result;
            }
            
            result.CardValidation = validationResult;
            result.ShouldPlayerChooseCard = true;
        }
        
        return result;
        
    }
    
    public GameEngineResults.ExitOrDrawResult HandleExitOrDraw(ValidateInputs.ValidationResult validation,
           Player player, ECardColor? declaredColor, string? userInput = null)
    {
        var result = new GameEngineResults.ExitOrDrawResult();
        
        if (validation.InputLetter == "x" && validation.IsValid)
        {
            State.ExitGame = true;
            result.ExitGame = true;
            return result;
        }
    
        if ((validation.InputLetter == "d" && validation.IsValid) || State.CurrentPlayer!.PlayerType == EPlayerType.AI
                                                                  || userInput == "d")
        {
            result.DrawCard = true;
            return result;
        }
    
        return result;
    }

    public GameCard? CheckIfForceDrawPlay(PlayerTurn turn)
    {
        if (turn.Result == TurnResult.ForceDrawPlay)
        {
            return turn.Card;
        }

        return null;
    }
    
    public List<GameCard> PlayableCards(Player player, ECardColor? declaredColor)
    {
        var playableCards = new List<GameCard>();
        foreach (var card in player.Hand!)
        {
            if (IsValidCardSelection(card, declaredColor).IsValid && PlayMatchingCard(card, declaredColor).IsCardPlayable)
            {
                playableCards.Add(card);
            }
        }

        return playableCards;
    }

    public GameEngineResults.IsValidCardSelectionResult IsValidCardSelection(GameCard selectedCard, ECardColor? declaredColor)
    {
        var result = new GameEngineResults.IsValidCardSelectionResult();
        
        if (State.PlayerTurns.Any() && State.PlayerTurns.Peek().StackCards)
        {
            if ((State.PlayerTurns.Peek().Result == TurnResult.DrawTwo
                 && selectedCard.CardValue != ECardValue.DrawTwo) ||
                (State.PlayerTurns.Peek().Result == TurnResult.WildDrawFour
                 && selectedCard.CardValue != ECardValue.DrawFour))
            {
                result.StackCardsNotValid = true;
                return result;
            }
        }
    
        if (declaredColor != null && selectedCard.CardColor != declaredColor
                                  && selectedCard.CardColor != ECardColor.Wild)
        {
            result.DeclaredColorNotValid = true;
            result.IsValid = false;
            return result;
        }

        result.IsValid = true;
        return result;
    }
    
    public GameEngineResults.PlayMatchingCardResult PlayMatchingCard(GameCard? selectedCardByPlayer,
                                                                     ECardColor? declaredColor = null)
    {
        var result = new GameEngineResults.PlayMatchingCardResult();
        
        if (selectedCardByPlayer == null)
        {
            var turn = PlayNoMatchingDrawnCard(declaredColor);
            result.PlayNoMatchingCard = true;
            result.PlayerTurn = turn;
            return result;
        }

        if (State.Rules.IsHouseRuleActive(EHouseRules.SevenO) && State.PlayerTurns.Any() &&
            (selectedCardByPlayer.CardValue == ECardValue.Seven
             || selectedCardByPlayer.CardValue == ECardValue.Zero))
        {
            result.IsCardPlayable = true;
            result.PlayCard = true;
            result.SelectedCard = selectedCardByPlayer;
            return result;
        }

        switch (selectedCardByPlayer.CardValue)
        {
            case ECardValue.DrawFour:
            case ECardValue.DrawTwo when IsMatchingCard(selectedCardByPlayer):
            case ECardValue.Wild:
            case ECardValue.Skip when IsMatchingCard(selectedCardByPlayer):
            case ECardValue.Reverse when IsMatchingCard(selectedCardByPlayer):
                result.IsCardPlayable = true;
                result.PlayCard = true;
                result.SelectedCard = selectedCardByPlayer;
                return result;
            default:
                if (IsMatchingCard(selectedCardByPlayer))
                {
                    result.IsCardPlayable = true;
                    result.PlayCard = true;
                    result.SelectedCard = selectedCardByPlayer;
                    return result;
                }

                result.IsCardPlayable = false;
                return result;
        }
    }

    private bool IsMatchingCard(GameCard selectedCard)
    {
        return selectedCard.CardColor == State.CurrentPlayCardOnTheTable!.CardColor
            || selectedCard.CardValue == State.CurrentPlayCardOnTheTable!.CardValue
            || State.CurrentPlayCardOnTheTable!.CardColor == ECardColor.Wild;
    }
    
    public GameEngineResults.HandleDeclareColorResult DeclareColor(PlayerTurn turn, string? userInput = null)
    {
        var declareColorResult = new GameEngineResults.HandleDeclareColorResult();

        var validate = Validate.ValidateAndPromptInput(
            "Please choose color:", null,  minRange: 1, maxRange: 4,
                                        inputMode: ValidateInputs.InputMode.NumberOnly, userInput: userInput);

        if (validate.IsValid && validate.InputNumber != null)
        {
            turn!.DeclaredColor = (ECardColor) validate.InputNumber - 1;
            declareColorResult.PlayerTurn = turn;
        }

        return declareColorResult;
    }

    public GameEngineResults.DeclareColorBeforeValidationResult DeclareColorBeforeValidation(PlayerTurn turn)
    {
        
        var result = new GameEngineResults.DeclareColorBeforeValidationResult();
        
        if (!State.PlayerTurns.Any() && turn.Card!.CardColor == ECardColor.Wild)
        {
            result.PromptPlayerTurn = true;
        }
        
        var list = PossibleColors();

        result.CardColors = list;
        return result;
    }

    public List<ECardColor> PossibleColors()
    {
        List<ECardColor> list = new List<ECardColor>();
        foreach (ECardColor color in Enum.GetValues(typeof(ECardColor)))
        {
            if (color != ECardColor.Wild)
            {
                list.Add(color);
            }
        }

        return list;
    }

    public GameEngineResults.HandlePlayCardResult PlayCard(Player player, GameCard selectedCardByPlayer)
    {
        var result = new GameEngineResults.HandlePlayCardResult();
        
        PlayerTurn turn = new PlayerTurn
        {
            Card = selectedCardByPlayer,
            Player = player,
            Result = GetTurnResult(selectedCardByPlayer)
        };

        player.Hand!.Remove(selectedCardByPlayer);

        if (State.PlayerTurns.Any() && State.PlayerTurns.Peek().StackCards)
        {
            turn.StackCards = true;
            turn.StackCount = State.PlayerTurns.Peek().StackCount + 1;
        }

        if (turn.Result == TurnResult.WildDrawFour || turn.Result == TurnResult.DrawTwo)
        {
            var matchingCards = FindMatchingCards(player);
            turn.DidCheat = !matchingCards.All(x => x.CardValue == selectedCardByPlayer.CardValue
                                                    && x.CardColor == State.CurrentPlayCardOnTheTable!.CardColor);
        }

        if (turn.Result == TurnResult.WildCard || turn.Result == TurnResult.WildDrawFour)
        {
            result.ShouldDeclareColor = true;
        }

        if (turn.Result == TurnResult.PlayedCard && selectedCardByPlayer.CardValue == ECardValue.Seven
                                                 && State.Rules.IsHouseRuleActive(EHouseRules.SevenO))
        {
            result.ShouldSwapHandsWithAnotherPlayer = true;
        }

        if (turn.Result == TurnResult.PlayedCard && selectedCardByPlayer.CardValue == ECardValue.Zero
                                                 && State.Rules.IsHouseRuleActive(EHouseRules.SevenO))
        {
            result.ShouldSwapAllHands = true;
        }
        // if (player.PlayerType == EPlayerType.AI)
        // {
        //     var mostColoredCards = player.Hand!
        //         .GroupBy(x => x.CardColor)
        //         .OrderByDescending(x => x.Count());
        //
        //     turn.DeclaredColor = mostColoredCards.First().First().CardColor;
        // }

        State.CurrentPlayCardOnTheTable = selectedCardByPlayer;
        State.DiscardPile.Add(selectedCardByPlayer);
        State.PlayerTurns.Push(turn);
        State.Players[State.PlayerIndex] = player;
        
        result.PlayerTurn = turn;
        return result;
    }

    private TurnResult GetTurnResult(GameCard selectedCardByPlayer)
    {
        return selectedCardByPlayer.CardValue switch
        {
            ECardValue.DrawFour => TurnResult.WildDrawFour,
            ECardValue.DrawTwo => TurnResult.DrawTwo,
            ECardValue.Wild => TurnResult.WildCard,
            ECardValue.Skip => TurnResult.Skip,
            ECardValue.Reverse => TurnResult.Reversed,
            _ => TurnResult.PlayedCard
        };
    }
    
    public GameEngineResults.HandleSwapHandsWithAnotherPlayerResult SwapHandsWithAnotherPlayer(Player player,
                                                                                    string? userInput = null)
    {
        var result = new GameEngineResults.HandleSwapHandsWithAnotherPlayerResult();
        var players = State.Players.Where(p => p != player).ToList();
        if (player.PlayerType == EPlayerType.AI)
        {
            players.Remove(player);
        }
        int index = player.PlayerType == EPlayerType.AI ? new Random().Next(players.Count) :
            Validate.ValidateAndPromptInput(
            "Choose a player to swap hands with:", null,
            minRange: 1, maxRange: players.Count, inputMode: ValidateInputs.InputMode.NumberOnly,
            userInput: userInput).InputNumber!.Value - 1;

        if (index >= 0 && index < players.Count)
        {
            (players[index].Hand, player.Hand) = (player.Hand, players[index].Hand);
            result.SwappedWithPlayer = players[index];
        }
        else
        {
            result.CannotChooseSelf = true;
        }

        return result;
    }

    // public GameEngineResults.HandleSwapHandsWithAnotherPlayerResult SwapHandsWithAnotherPlayer(Player player)
    // {
    //     var result = new GameEngineResults.HandleSwapHandsWithAnotherPlayerResult();
    //
    //     if (player.PlayerType == EPlayerType.AI)
    //     {
    //         Random random = new Random();
    //         var players = State.Players;
    //         players.Remove(player);
    //         int randomPlayerIndex = random.Next(0, players.Count);
    //         
    //         (State.Players[randomPlayerIndex].Hand, player.Hand) =
    //             (player.Hand, State.Players[randomPlayerIndex].Hand);
    //         
    //         result.SwappedWithPlayer = State.Players[randomPlayerIndex];
    //         return result;
    //     }
    //     
    //     var validationResult = Validate.ValidateAndPromptInput(
    //         "Choose a player to swap hands with:", null,
    //         minRange: 1, maxRange: State.Players.Count, inputMode: ValidateInputs.InputMode.NumberOnly);
    //
    //     if (validationResult.IsValid && validationResult.InputNumber != null)
    //     {
    //         if (State.Players[validationResult.InputNumber.Value - 1] == player)
    //         {
    //             result.CannotChooseSelf = true;
    //         }
    //         else
    //         {
    //             (State.Players[validationResult.InputNumber.Value - 1].Hand, player.Hand) =
    //                 (player.Hand, State.Players[validationResult.InputNumber.Value - 1].Hand);
    //         
    //             result.SwappedWithPlayer = State.Players[validationResult.InputNumber.Value - 1];
    //         }
    //     }
    //      
    //     return result;
    // }
    
    public PlayerTurn PlayNoMatchingDrawnCard(ECardColor? declaredColor)
    {
        var turn = new PlayerTurn();
        turn.Card = State.CurrentPlayCardOnTheTable!;
        turn.Result = TurnResult.ForceDraw;
        turn.Player = State.CurrentPlayer;
        turn.DeclaredColor = declaredColor;
        
        State.PlayerTurns.Push(turn);
        return turn;
    }
    
    public void SwapAllHands(DirectionOfPlay direction)
    {
        int playerCount = State.Players.Count;
        
        if (direction == DirectionOfPlay.Clockwise)
        {
            // Temporarily hold the hand of the first player
            var lastPlayerHand = State.Players[playerCount - 1].Hand;

            // Move each hand to the next player
            for (int i = playerCount - 1; i > 0; i--)
            {
                State.Players[i].Hand = State.Players[i - 1].Hand;
            }

            // Set the last player's hand to what was the first player's hand
            State.Players[0].Hand = lastPlayerHand;
        }

        if (direction == DirectionOfPlay.CounterClockwise)
        {
            var firstPlayerHand = State.Players[0].Hand;
            
            for (int i = 0; i < playerCount - 1; i++)
            {
                State.Players[i].Hand = State.Players[i + 1].Hand;
            }
            
            State.Players[playerCount - 1].Hand = firstPlayerHand;
        }
    }

    public List<GameCard> FindMatchingCards(Player player)
    {
        var matchingCards = player.Hand!.Where(x =>
            x.CardColor == State.CurrentPlayCardOnTheTable!.CardColor
            || x.CardValue == State.CurrentPlayCardOnTheTable!.CardValue
            || x.CardColor == ECardColor.Wild).ToList();
        
        return matchingCards;
    }
    
        
    public GameEngineResults.DrawCardResult DrawCard(Player player, ECardColor? declaredColor)
    {
        var result = new GameEngineResults.DrawCardResult();
        PlayerTurn turn = new PlayerTurn { Player = player };
        var drawnCard = Draw(1).FirstOrDefault();

        if (drawnCard == null)
        {
            result.IsOutOfCards = true;
            result.PlayerTurn = turn;
            return result;
        }

        result.DrawnCard = drawnCard;

        if (CanPlayDrawnCard(drawnCard, declaredColor))
        {
            turn.Card = drawnCard;
            turn.Result = TurnResult.ForceDrawPlay;
            result.CanPlayDrawnCard = true;
        }
        else
        {
            player.Hand?.Add(drawnCard);
            turn.Result = TurnResult.ForceDraw;
            turn.Card = State.CurrentPlayCardOnTheTable!;
            result.CannotPlayDrawnCard = true;
        }

        result.PlayerTurn = turn;
        return result;
    }

    private bool CanPlayDrawnCard(GameCard drawnCard, ECardColor? declaredColor)
    {
        return (declaredColor != null && Utilities.HasMatch((ECardColor)declaredColor,
                                                            drawnCard.CardColor))
            || (declaredColor == null && Utilities.HasMatch(State.CurrentPlayCardOnTheTable!, drawnCard));
    }
    
    public string InitializeDeck(Rules ruleSettings)
    {
        foreach (ECardColor color in Enum.GetValues(typeof(ECardColor)))
        {
            if (color != ECardColor.Wild)
            {
                AddNumberedCards(color);
                AddSpecialCards(color);
                AddZeroCard(color);
            }
            else if (!ruleSettings.NoWildCardsInPlay)
            {
                AddWildCards(color);
            }
        }

        return $"Cards initialized. There are {State.DrawPile.Count} cards in draw pile";
    }

    private void AddNumberedCards(ECardColor color)
    {
        for (int i = 1; i <= 9; i++)
        {
            AddCard(color, (ECardValue)i, i, 2);
        }
    }

    private void AddSpecialCards(ECardColor color)
    {
        foreach (ECardValue val in new[] { ECardValue.Skip, ECardValue.Reverse, ECardValue.DrawTwo })
        {
            AddCard(color, val, 20, 2);
        }
    }

    private void AddZeroCard(ECardColor color)
    {
        AddCard(color, ECardValue.Zero, 0, 1);
    }

    private void AddWildCards(ECardColor color)
    {
        foreach (ECardValue val in new[] { ECardValue.Wild, ECardValue.DrawFour })
        {
            AddCard(color, val, 50, 4);
        }
    }

    private void AddCard(ECardColor color, ECardValue value, int score, int count)
    {
        var displayColor = "";
        displayColor = color == ECardColor.Red ? "red" : displayColor;
        displayColor = color == ECardColor.Blue ? "blue" : displayColor;
        displayColor = color == ECardColor.Green ? "green" : displayColor;
        displayColor = color == ECardColor.Yellow ? "yellow" : displayColor;
        
        var specialCard = "";
        specialCard = value == ECardValue.Skip ? "skip" : specialCard;
        specialCard = value == ECardValue.Reverse ? "reverse" : specialCard;
        specialCard = value == ECardValue.DrawTwo ? "plus-two" : specialCard;
        
        string visual = "";
        
        for (int i = 0; i < count; i++)
        {
            if (value == ECardValue.Reverse)
            {
                visual = 
                    $@"<div class=""card {displayColor}"">
                            <div class=""ellipse""></div>
                            <div class=""content {displayColor}"">
                                <div class=""reverse"">
                                    <div class=""arrows"">
                                        <div class=""arrow""></div>
                                        <div class=""arrow""></div>
                                    </div>
                                </div>
                            </div>
                            <div class=""small-content {displayColor}"">
                                <div class=""reverse"">
                                    <div class=""arrows"">
                                        <div class=""arrow""></div>
                                        <div class=""arrow""></div>
                                    </div>
                                </div>
                            </div>
                            <div class=""small-content-reverse {displayColor}"">
                                <div class=""reverse"">
                                    <div class=""arrows"">
                                        <div class=""arrow""></div>
                                        <div class=""arrow""></div>
                                    </div>
                                </div>
                            </div>
                        </div>"; 
            }
            else if (value == ECardValue.Skip)
            {
                visual = 
                    $@"<div class='card {displayColor}'>
                <div class='ellipse'></div>
                    <div class='content {displayColor}'>
                        <div class='{specialCard}'></div>
                    </div>
                    <div class='small-content {displayColor}'>
                        <div class='{specialCard}'></div>
                    </div>
                    <div class='small-content-reverse {displayColor}'>
                        <div class='{specialCard}'></div>
                    </div>
                </div>"; 
            }
            
            else if (value == ECardValue.DrawTwo)
            {
                visual = 
                    $@"<div class='card {displayColor}'>
                        <div class='ellipse'></div>
                        <div class='content {displayColor}'>
                            <div class='plus-two'>
                                <div class='plus-two-before'></div>
                                <div class='plus-two-after'></div>
                            </div>
                        </div>
                        <div class='small-content {displayColor}'>
                            <div class='plus-two'>+2
                                <div class='plus-two-before'></div>
                                <div class='plus-two-after'></div>
                            </div>
                        </div>
                        <div class='small-content-reverse {displayColor}'>
                            <div class='plus-two'>+2
                                <div class='plus-two-before'></div>
                                <div class='plus-two-after'></div>
                            </div>
                        </div>
                    </div>"; 
            }

            else if (value == ECardValue.Wild)
            {
                visual = 
                     $@"<div class='card black'>
                         <div class='ellipse'></div>
                         <div class='content black'>
                             <div class='wild'>
                                 <div class='segment red'></div>
                                 <div class='segment blue'></div>
                                 <div class='segment green'></div>
                                 <div class='segment yellow'></div>
                             </div>
                         </div>
                         <div class='small-content black'>
                             <div class='wild'>
                                 <div class='segment red'></div>
                                 <div class='segment blue'></div>
                                 <div class='segment green'></div>
                                 <div class='segment yellow'></div>
                             </div>
                         </div>
                         <div class='small-content-reverse black'>
                             <div class='wild'>
                                 <div class='segment red'></div>
                                 <div class='segment blue'></div>
                                 <div class='segment green'></div>
                                 <div class='segment yellow'></div>
                             </div>
                         </div>
                     </div>"; 
            }
            else if (value == ECardValue.DrawFour)
            {
                visual = 
                    $@"<div class='card black'>
                        <div class='ellipse'></div>
                        <div class='content green'>
                            <div class='plus-four'>
                                <div class='card1'></div>
                                <div class='card2'></div>
                                <div class='card3'></div>
                                <div class='card4'></div>
                            </div>
                        </div>
                    </div>"; 
            }

            else
            {
                visual = $@"
                <div class='card {displayColor}'>
                    <div class='ellipse'></div>
                    <div class='content {displayColor}'>
                        <div class='number'>{(int)value}</div>
                    </div>
                    <div class='small-content {displayColor}'>
                        <div class='number'>{(int)value}</div>
                    </div>
                    <div class='small-content-reverse {displayColor}'>
                        <div class='number'>{(int)value}</div>
                    </div>
                </div>";
            }
            
            
            State.DrawPile.Add(new GameCard()
            {
                CardColor = color,
                CardValue = value,
                Score = score,
                DisplayCard = visual
                
            });
        }
    }
    
    //Fisher-Yates shuffle algorithm
    public string ShuffleCards()
    {
        Random r = new Random();
        List<GameCard> cards = State.DrawPile;

        int n = cards.Count;
        while (n > 1)
        {
            n--;
            int k = r.Next(n + 1);
            GameCard temp = cards[n];
            cards[n] = cards[k];
            cards[k] = temp;
        }
        
        return "Cards shuffled";
    }
    
    private void ReshuffleCards()
    {
        var currentCard = State.DiscardPile[^1];
        State.DiscardPile.RemoveAt(State.DiscardPile.Count - 1);
        State.DrawPile = State.DiscardPile;
        ShuffleCards();
        State.DiscardPile = new List<GameCard>();
        State.DiscardPile.Add(currentCard);
    }
    
    public List<GameCard> Draw(int count)
    {
        var drawnCards = new List<GameCard>();
        int cardsToTake = count;
        
        if (cardsToTake > State.DrawPile.Count && State.DrawPile.Count != 0)
        {
            // Take all cards from the remaining draw pile
            drawnCards = State.DrawPile;
            cardsToTake -= drawnCards.Count;
            State.DrawPile.Clear();
        }

        if (State.DrawPile.Count == 0)
        {
            ReshuffleCards();
        }
        
        var takenCards = State.DrawPile.Take(cardsToTake).ToList();
        drawnCards.AddRange(takenCards);
    
        State.DrawPile.RemoveAll(x => takenCards.Contains(x));
        
        return drawnCards;
    }
    
    public bool IsSpecialCard(ECardValue cardValue)
    {
        return cardValue == ECardValue.Wild
               || cardValue == ECardValue.Skip
               || cardValue == ECardValue.Reverse
               || cardValue == ECardValue.DrawTwo
               || cardValue == ECardValue.DrawFour;
    }
    
    public string DetermineDealer()
    {
        StringBuilder message = new StringBuilder();

        message.AppendLine("Let's find out who is the dealer");

        DealOneCardToEachPlayer();

        List<Player> highestValuePlayers = GetPlayersWithHighestCard();

        while (highestValuePlayers.Count > 1)
        {
            message.AppendLine($"{string.Join(", ", highestValuePlayers.Select(p => p.NickName))}" +
                               $" had the same cards! Card: {highestValuePlayers.First().Hand!.First().CardValue}");
            message.AppendLine("They will take new cards from draw pile");

            var reDeal = ReDealCardsToDetermineDealer(highestValuePlayers);
            if (reDeal != null)
            {
                message.AppendLine(reDeal);
            }
            highestValuePlayers = GetPlayersWithHighestCard();

            if (State.DrawPile.Count == 0)
            {
                message.AppendLine("No more cards left in the draw pile!");
                message.AppendLine("Dealer will be randomly picked.");

                State.Dealer = highestValuePlayers[new Random().Next(highestValuePlayers.Count)];
            }
        }

        State.DrawPile.AddRange(State.DiscardPile);
        State.DiscardPile.Clear();
        State.Dealer = highestValuePlayers.First();

        message.AppendLine($"{State.Dealer.NickName} has the highest card and is the dealer!" +
                           $" Winning card: {State.Dealer.Hand!.First().CardValue}");
        
        return message.ToString();
    }

    private List<Player> GetPlayersWithHighestCard()
    {
        int highestCardValue = State.Players.Max(player => (int)player.Hand!.First().CardValue);
        return State.Players.Where(player => (int)player.Hand!.First().CardValue == highestCardValue).ToList();
    }

    public string? ReDealCardsToDetermineDealer(List<Player> highestValuePlayers)
    {
        foreach (var player in highestValuePlayers)
        {
            while (true)
            {
                var drawnCards = Draw(1);
                if (drawnCards.Any())
                {
                    var drawnCard = drawnCards.First();
                    if (!IsSpecialCard(drawnCard.CardValue) && (player.Hand = drawnCards) != null)
                    {
                        State.DiscardPile.Add(drawnCard);
                        State.Players.First(p => p.NickName == player.NickName).Hand = drawnCards;
                        return $"{player.NickName} takes card: {player.Hand.First().CardValue}";
                    }
                }
            }
        }

        return null;
    }

    public void DealOneCardToEachPlayer()
    {
        int count = 0;
        
        while (count < State.Players.Count)
        {
            List<GameCard> cards = Draw(1);
            GameCard card = cards.First();

            if (IsSpecialCard(card.CardValue))
            {
                State.DrawPile.Add(card);
                continue;
            }

            State.Players[count].Hand = cards;
            State.DiscardPile.Add(card);
            count++;
        }
    }


    public string DealCards(Rules ruleSettings)
    {
        StringBuilder message = new StringBuilder();
        message.AppendLine("Dealer deals the cards");
        
        foreach (var player in State.Players)
        {
            for (int j = 0; j < ruleSettings.PlayerHandSize; j++)
            {
                List<GameCard> cards = Draw(1);
                player.Hand!.AddRange(cards);

            }
        }

        if (State.DrawPile.Count == 108 - State.Players.Count * 7)
        {
            message.AppendLine($"{State.Players.Count * 7} cards was dealt to players");
        }

        return message.ToString();
    }

    public string FlipCard()
    {
        GameCard startingCard;
        do
        {
            startingCard = Draw(1).First();
            if (startingCard.CardValue == ECardValue.DrawFour)
            {
                State.DrawPile.Add(startingCard);
            }
        } while (startingCard.CardValue == ECardValue.DrawFour);

        State.DiscardPile = new List<GameCard> { startingCard };
        State.CurrentPlayCardOnTheTable = startingCard;

        return $"Flipped card from the top of the draw pile is:" +
                          $" {startingCard.CardValue}, {startingCard.CardColor}";
    }

    public string SetPlayDirection()
    {
        State.DirectionOfPlay = State.CurrentPlayCardOnTheTable!.CardValue == ECardValue.Reverse 
            ? DirectionOfPlay.CounterClockwise 
            : DirectionOfPlay.Clockwise;

        return $"The game's direction of play is" +
                          $" {(State.DirectionOfPlay == DirectionOfPlay.CounterClockwise
                              ? "counter-clockwise"
                              : "clockwise")}";
    }

    public string ClearAllPlayerHands()
    {
        foreach (var player in State.Players)
        {
            player.Hand?.Clear();
        }
        
        return "Players give all of their cards back";
    }
    
    public GameEngineResults.CheckIfLastPlayerShoutedUnoResult HandleIfLastPlayerShoutedUno(PlayerTurn previousTurn,
                                                                                          string? userInput = null)
    {
        GameEngineResults.CheckIfLastPlayerShoutedUnoResult result =
        new GameEngineResults.CheckIfLastPlayerShoutedUnoResult();
        ValidateInputs.ValidationResult valResult = new ValidateInputs.ValidationResult();

        if (State.CurrentPlayer!.PlayerType == EPlayerType.Human && State.PlayerTurns.Count > 1)
        {
            valResult = Validate.ValidateAndPromptInput(
            "IF THE LAST PLAYER SHOULD HAVE SHOUTED UNO, PRESS 'c'. TO CONTINUE PRESS 'ENTER'",
            new List<string> { "c" }, canBeEmptyString: true,
            inputMode: ValidateInputs.InputMode.LetterOnly, userInput: userInput);
        }
        
        if (State.PlayerTurns.Count > 1 && !previousTurn.DidShoutUno && previousTurn.Player?.Hand?.Count == 1)
        {
            if (valResult.InputLetter == "c" || State.CurrentPlayer!.PlayerType == EPlayerType.AI)
            {
                previousTurn.Player.Hand.AddRange(Draw(2));
                result.ShouldDrawCards = true;
            }
        }
        
        return result;
    }
    
    public GameEngineResults.HandleFirstTurnResult HandleFirstTurn()
    {
        var result = new GameEngineResults.HandleFirstTurnResult();
        
        if (!State.PlayerTurns.Any())
        {
            State.CurrentPlayer = State.Dealer!;
            State.PlayerIndex = State.CurrentPlayer.Position - 1;

            if (State.CurrentPlayCardOnTheTable!.CardValue != ECardValue.Reverse)
            {
                State.PlayerIndex = NextPlayerIndex(State.PlayerIndex);
                State.CurrentPlayer = State.Players[State.PlayerIndex];
            }

            result.ShouldPlayMatchingCard = true;
        }

        return result;
    }

    public GameEngineResults.DeclareWinnerIfNoMoreCardsLeftResult DeclareWinnerIfNoMoreCardsLeft()
    {
        var winningPlayer = State.Players.OrderBy(player => player.Hand!.Count)
            .ThenBy(player => player.Hand!.Sum(card => (int)card.CardValue))
            .First();

        winningPlayer.Score += State.Players.Sum(player => player.Hand!.Sum(x => x.Score))
                                          - winningPlayer.Hand!.Sum(x => x.Score);

        State.GameRounds.Add(State.PlayerTurns);
        State.RoundOver = true;
        State.Winner = winningPlayer;

        return new GameEngineResults.DeclareWinnerIfNoMoreCardsLeftResult
        {
            WinningPlayer = winningPlayer,
            Score = winningPlayer.Score,
        };
    }
    
    public void ResetGameState()
    {
        State.DrawPile.Clear();
        State.DiscardPile.Clear();
        State.PlayerTurns.Clear();
        ResetStateProperties();
    }

    public void ResetStateProperties()
    {
        State.CurrentPlayCardOnTheTable = default;
        State.CurrentPlayer = default;
        State.PlayerIndex = default;
        State.DirectionOfPlay = default;
        State.ExitGame = default;
        State.RoundOver = default;
    }
    
    public bool IsRoundOver()
    {
        if (State.DrawPile.Count == 0 && State.DiscardPile.Count == 1)
        {
            return true;
        }
        return false;
    }
    
    private bool ValidateUnoShout(string? userInput = null)
    {
        return Validate.ValidateAndPromptInput(
            "PRESS 'S' TO SHOUT UNO OR 'ENTER' TO CONTINUE", 
            new List<string> { "s" },
            canBeEmptyString: true, 
            inputMode: ValidateInputs.InputMode.LetterOnly, 
            userInput: userInput
        ).InputLetter is "s";
    }
    
    public void HandleUnoShout(PlayerTurn previousTurn, string? userInput = null)
    {
        if ((State.CurrentPlayer!.PlayerType == EPlayerType.Human && ValidateUnoShout(userInput))
            || previousTurn.Player?.Hand?.Count == 1)
        {
            previousTurn.DidShoutUno = true;
            if (State.PreviousTurn != null)
            {
                State.PreviousTurn.DidShoutUno = true;
            }
        }
        // else if (previousTurn.Player?.Hand?.Count == 1)
        // {
        //     previousTurn.DidShoutUno = true;
        // }
    }
    
    // public void HandleUnoShout(PlayerTurn previousTurn, string? userInput = null)
    // {
    //     if (State.CurrentPlayer!.PlayerType == EPlayerType.Human && Validate.ValidateAndPromptInput(
    //             "PRESS 'S' TO SHOUT UNO OR 'ENTER' TO CONTINUE", new List<string> { "s" },
    //             canBeEmptyString: true, inputMode: ValidateInputs.InputMode.LetterOnly, userInput: userInput
    //         ).InputLetter is "s")
    //     {
    //         previousTurn.DidShoutUno = true;
    //     }
    //     else if (previousTurn.Player?.Hand?.Count == 1)
    //     {
    //         previousTurn.DidShoutUno = true;
    //     }
    // }
    
    public void ContinueOrExitGame(string? userInput = null)
    {
        if (State.Players.Any(x => x.PlayerType == EPlayerType.Human))
        {
            var validation = Validate.ValidateAndPromptInput(
                "Press 'ENTER' to continue or 'x' to exit to main menu", validLetters: new List<string> { "x" },
                canBeEmptyString: true, inputMode: ValidateInputs.InputMode.LetterOnly, userInput: userInput);

            if (validation.IsValid && validation.InputLetter == "x" && 
                Validate.ValidateAndPromptInput(
                    "Are you sure you want to exit to main menu? (y/n)", new List<string> { "y", "n" },
                    inputMode: ValidateInputs.InputMode.LetterOnly, userInput: userInput).InputLetter == "y")
            {
                State.ExitGame = true;
            }   
        }
    }
    
    public Player? DeclareWinner()
    {
        var winningPlayer = State.Players.FirstOrDefault(x => !x.Hand!.Any());

        if (winningPlayer != null)
        {
            int score = State.Players.Sum(player => player.Hand!.Sum(x => x.Score));
            winningPlayer.Score += score;
            State.GameRounds.Add(State.PlayerTurns);
            State.RoundOver = true;
            State.Winner = winningPlayer;
            return winningPlayer;
        }

        return null;
    }
    
    //AI player plays first DrawTwo, Skip or Reverse card, then regular cards,
    //then Wild and finally DrawFour if s/he has nothing else to play.
    public GameCard? PlayAiTurn(Player player, ECardColor? declaredColor)
    {
        if (State.PlayerTurns.Any() && State.PlayerTurns.Peek().StackCards)
        {
            if (State.PlayerTurns.Peek().Result == TurnResult.DrawTwo
                && player.Hand!.Any(x => x.CardValue == ECardValue.DrawTwo))
            {
                return player.Hand!.First(x => x.CardValue == ECardValue.DrawTwo);
            }
            if (State.PlayerTurns.Peek().Result == TurnResult.WildDrawFour
                && player.Hand!.Any(x => x.CardValue == ECardValue.DrawFour))
            {
                return player.Hand!.First(x => x.CardValue == ECardValue.DrawFour);
            }
        }
        
        if (declaredColor != null)
        {
            var matchingColorCard = player.Hand!.FirstOrDefault(x => x.CardColor == declaredColor);
            if (matchingColorCard != null)
            {
                return matchingColorCard;
            }
        }
        
        var matching = FindMatchingCards(player);
        
        var matchingColors = matching
            .Where(card => declaredColor != null && (card.CardColor == declaredColor || card.CardColor == ECardColor.Wild))
            .ToList();

        if (matchingColors.Any())
        {
            matching = matchingColors;
        }
        
        // matching = matchingColors.Any() ? matchingColors : matching;
        
        if (matching.Any())
        {
            if (matching.All(x => x.CardValue == ECardValue.DrawFour))
            {
                return player.Hand!.First(x => x.CardValue == ECardValue.DrawFour);
            }
            
            if (matching.Any(x => x.CardValue == ECardValue.DrawTwo))
            {
                return matching.First(x => x.CardValue == ECardValue.DrawTwo);
            }
            if (matching.Any(x => x.CardValue == ECardValue.Skip))
            {

                return matching.First(x => x.CardValue == ECardValue.Skip);
            }
            if (matching.Any(x => x.CardValue == ECardValue.Reverse))
            {
                return matching.First(x => x.CardValue == ECardValue.Reverse);
            }
            
            GameCard? regularCard = matching.FirstOrDefault(x => x.CardColor != ECardColor.Wild
                                                                 && x.CardValue != ECardValue.DrawTwo
                                                                 && x.CardValue != ECardValue.Skip
                                                                 && x.CardValue != ECardValue.Reverse);

            if (regularCard != null)
            {
                return regularCard;
            }
            
            if (matching.Any(x => x.CardValue == ECardValue.Wild))
            {
                return matching.First(x => x.CardValue == ECardValue.Wild);
            }
        }
        
        return null;
    }


    public GameEngineResults.PlayerChooseCardResult AiChooseCard(Player player, ECardColor? declaredColor)
    {
        var gameCard = PlayAiTurn(player, declaredColor);
        var result = new GameEngineResults.PlayerChooseCardResult();

        if (gameCard == null)
        {
            result.ShouldExitOrDraw = true;
            return result;
        }
        
        var validationResult = IsValidCardSelection(gameCard, declaredColor);
        if (validationResult.IsValid)
        {
            result.CardValidation = validationResult;
            result.IsValidCardSelection = true;
            result.SelectedCard = gameCard;
        }
        else
        {
            result.ShouldExitOrDraw = true;
        }

        return result;
    }
    
    public ECardColor AiColorDeclaration(Player player)
    {
        var random = new Random();
        var choice = random.Next(0, 4);
        
        var mostColoredCards = player.Hand!
            .Where(x => x.CardColor != ECardColor.Wild)
            .GroupBy(x => x.CardColor)
            .OrderByDescending(x => x.Count()).ToList();
    
        return mostColoredCards.Any() ? mostColoredCards.First().First().CardColor : (ECardColor)choice;
    }
}
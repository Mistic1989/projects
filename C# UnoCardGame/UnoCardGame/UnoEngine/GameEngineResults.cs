using Domain;

namespace UnoEngine;

public class GameEngineResults
{
    // public class PreviousTurnResult
    // {
    //     public PlayerTurn? PlayerTurn { get; set; }
    //     public bool IsPlayDirectionReversed { get; set; }
    //     public bool DidShoutUno { get; set; }
    // }
    
    public class HandlePreviousTurnResult
    {
        public PlayerTurn? PlayerTurn { get; set; }
        public bool IsPlayerAttacked { get; set; }
    }
    
    public class HandlePlayerAttackResult
    {
        public PlayerTurn? PreviousTurn { get; set; }
        public Player? Player { get; set; }
        public bool ShouldPromptForStacking { get; set; }
        public bool ShouldHandleAttackByPreviousPlayer { get; set; }
        public bool ShouldSwitchToNextPlayer { get; set; }
    }
    
    public class HandleAttackByPreviousPlayerResult
    {
        public PlayerTurn? PreviousTurn { get; set; }
        public Player? Player { get; set; }
        public bool ShouldHandleSkipCard { get; set; }
        public bool ShouldHandleDrawTwoCard { get; set; }
        public bool ShouldHandleDrawFourCard { get; set; }
        
        public int StackCount { get; set; }
    }
    
    public class HandleChallengeResult
    {
        public PlayerTurn? PlayerTurn { get; set; }
        public bool DidCheat { get; set; }
        public bool WasChallengeSuccessful { get; set; }
        public GameCard? PenultimateCard { get; set; }
    }
    
    public class HandleDrawFourCardResult
    {
        public PlayerTurn? PlayerTurn { get; set; }
        public int StackCount { get; set; }
        public bool ShouldHandleChallenge { get; set; }
        public bool ShouldDrawCards { get; set; }
        public ValidateInputs.ValidationResult ValidationResult { get; set; }
        public Player? PreviousPlayer { get; set; }
    }
    
    
    public class DeclareWinnerIfNoMoreCardsLeftResult
    {
        public Player? WinningPlayer { get; set; }
        public int Score { get; set; }
    }
    
    public class CheckIfLastPlayerShoutedUnoResult
    {
        public bool ShouldDrawCards { get; set; }
    }
    
    public class PlayMatchingCardResult
    {
        public PlayerTurn? PlayerTurn { get; set; }
        public bool IsCardPlayable { get; set; }
        public string? Message { get; set; }
        public bool PlayerChooseCard { get; set; }
        public bool PlayNoMatchingCard { get; set; }
        public bool PlayCard { get; set; }
        public GameCard? SelectedCard { get; set; }
    }
    
    public class PlayerChooseCardResult
    {
        public ValidateInputs.ValidationResult ValidationResult { get; set; }
        public GameCard? SelectedCard { get; set; }
        public bool ShouldExitOrDraw { get; set; }
        public bool IsValidCardSelection { get; set; }
        public bool ShouldPlayerChooseCard { get; set; }

        public IsValidCardSelectionResult CardValidation { get; set; } = new IsValidCardSelectionResult();
        // public PlayerTurn? PlayerTurn { get; set; }
        // public bool PlayNoMatchingCard { get; set; }
    }
    
    public class ExitOrDrawResult
    {
        public bool ExitGame { get; set; }
        public bool DrawCard { get; set; }
    }
    
    public class DrawCardResult
    {
        public PlayerTurn? PlayerTurn { get; set; }
        public bool CanPlayDrawnCard { get; set; }
        public bool IsOutOfCards { get; set; }
        public bool CannotPlayDrawnCard { get; set; }
        public GameCard? DrawnCard { get; set; }
    }
    
    public class HandlePlayCardResult
    {
        public PlayerTurn? PlayerTurn { get; set; }
        public bool ShouldDeclareColor { get; set; }
        public bool ShouldSwapHandsWithAnotherPlayer { get; set; }
        public bool ShouldSwapAllHands { get; set; }
    }
    
    public class HandleDeclareColorResult
    {
        public PlayerTurn? PlayerTurn { get; set; }
    }
    
    public class DeclareColorBeforeValidationResult
    {
        public List<ECardColor>? CardColors { get; set; }
        public bool PromptPlayerTurn { get; set; }
    }
    
    public class HandleSwapHandsWithAnotherPlayerResult
    {
        public Player? SwappedWithPlayer { get; set; }
        public bool CannotChooseSelf { get; set; }
    }
    
    public class HandleFirstTurnResult
    {
        public bool ShouldPlayMatchingCard { get; set; }
    }
    
    public class IsValidCardSelectionResult
    {
        public bool IsValid { get; set; }
        public bool DeclaredColorNotValid { get; set; }
        public bool StackCardsNotValid { get; set; }
    }
}
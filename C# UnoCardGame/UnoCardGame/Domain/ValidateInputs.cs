
namespace Domain;

public class ValidateInputs
{
    public enum InputMode
        {
            Any,
            NumberOnly,
            LetterOnly
        }
    
    public struct ValidationResult
    {
        public bool IsValid { get; set; }
        public string Message { get; set; }
        
        public int? InputNumber { get; set; }
        public string? InputLetter { get; set; }
    
        public ValidationResult(bool isValid, int? userInputNumber = null,
                      string? userInputLetter = null, string message = "")
        {
            IsValid = isValid;
            Message = message;
            InputNumber = userInputNumber;
            InputLetter = userInputLetter;
        }
    }

    public ValidationResult ValidateAndPromptInput(
    string? promptMessage,
    List<string>? validLetters, 
    int? minRange = null,
    int? maxRange = null,
    bool canBeEmptyString = false,
    InputMode inputMode = InputMode.Any,
    int? minLength = null,
    int? maxLength = null,
    string? userInput = null)
    {
        ValidationResult validationResult = new ValidationResult();
        string? input = userInput;
        
        do
        {
            if (userInput == null)
            {
                if (promptMessage != null)
                {
                    Console.WriteLine(promptMessage);
                }
                
                userInput = Console.ReadLine()?.Trim().ToLower();
            }
            else
            {
                userInput = userInput.Trim().ToLower();
            }

            if (string.IsNullOrWhiteSpace(userInput))
            {
                if (canBeEmptyString)
                {
                    return new ValidationResult(true, userInputLetter: userInput);
                }
                validationResult = new ValidationResult(false, message: "Input cannot be empty or whitespace.");
            }
            else
            { 
                if (minLength.HasValue && userInput.Length < minLength.Value)
                {
                    validationResult = new ValidationResult(false, message: $"Input is too short. Minimum length allowed is {minLength.Value}.");
                }

            
                if (maxLength.HasValue && userInput.Length > maxLength.Value)
                { 
                    validationResult = new ValidationResult(false, message: $"Input is too long. Maximum length allowed is {maxLength.Value}.");
                }

                bool isNumber = userInput.All(char.IsDigit);
                bool isLetter = userInput.All(char.IsLetter) && userInput.Length == 1;
                bool isString = minLength != null && minLength > 1 || maxLength != null && maxLength > 1;

                if (inputMode == InputMode.NumberOnly && !isNumber)
                {
                    validationResult = new ValidationResult(false, message: "Invalid input. Enter a number.");
                }

                if (inputMode == InputMode.LetterOnly && !isLetter)
                {
                    validationResult = new ValidationResult(false, message: "Invalid input. Enter a single letter from the valid list.");
                }

                if (inputMode == InputMode.Any && !isNumber && !isLetter && !isString)
                {
                    validationResult = new ValidationResult(false, message: "Invalid input. Enter either a single letter from the valid list or a number.");
                }

                if (isNumber)
                {
                    var numberValidationResult = ValidateNumberInput(userInput, minRange, maxRange);
                    if (!numberValidationResult.IsValid)
                    {
                        validationResult = new ValidationResult(false, message: numberValidationResult.Message);
                    }
                    else
                    {
                        validationResult = new ValidationResult(true, userInputNumber: int.Parse(userInput));
                    }
                }

                if (isLetter)
                {
                    var letterValidationResult = ValidateLetterInput(userInput, validLetters ?? new List<string>());
                    if (!letterValidationResult.IsValid)
                    {
                        validationResult = new ValidationResult(false, message: letterValidationResult.Message);
                    }
                    else
                    {
                        validationResult = new ValidationResult(true, userInputLetter: userInput);
                    }
                }

                if (isString)
                {
                    validationResult = new ValidationResult(true, userInputLetter: userInput);
                } 
            }
            
            if (input != null)
            {
                break;
            }
            
            if (!validationResult.IsValid)
            {
                Console.WriteLine(validationResult.Message);
                userInput = null;
            }
            
        } while (!validationResult.IsValid);

        return validationResult;
    }

    private ValidationResult ValidateNumberInput(string userInput, int? minRange, int? maxRange)
    {
        if (!int.TryParse(userInput, out var inputNumber))
        {
            return new ValidationResult(false, message: "Invalid number format.");
        }

        if (minRange.HasValue && inputNumber < minRange.Value)
        {
            return new ValidationResult(false,
                message: $"Number is too low. Minimum allowed is {minRange.Value}.");
        }

        if (maxRange.HasValue && inputNumber > maxRange.Value)
        {
            return new ValidationResult(false,
                message: $"Number is too high. Maximum allowed is {maxRange.Value}.");
        }

        return new ValidationResult(true, inputNumber);
    }

    private ValidationResult ValidateLetterInput(string userInput, List<string> validLetters)
    {
        if (!validLetters.Contains(userInput))
        {
            return new ValidationResult(false, userInputLetter: userInput,
                                   message: "You entered an incorrect letter.");
        }

        return new ValidationResult(true, userInputLetter: userInput);
    }
}
#Discord Bot Commands


Guide on using the bot:
Below are some of the currently implemented commands. (OUTDATED)

if the command has brackets [] around it, ex: '[getXKCD|xkcd]', any of the words within the brackets can be used, the words are separated using '|'. Ex. !xkcd and !getXKCD run the same command.

Some commands may accept input, parameters are shown after the inital !call to the command, seperated by spaces. To give the command input, you must provide all parameters unless otherwise noted. Exclude the arrows from the command call.
If a command accepts multiple parameters, the parameters are seperated using a space. Ex. '!weather 1 2' where 1 is parameter <lat> and 2 is parameter <lon>.

There are four different types of data commands accept currently. 

Integers: simply a number with NO decimal in it, 

strings: a string of characters ex `"This is a string of characters"`. If you want to use spaces in your string, you must surround the string with double quotes: "" 

float: decimal number

list: a list of items, must be passed as a string, elements being seperated by a command and a space. ex:
"dog, cat, lizard"

parameter input types are described in the description of the command.
## Vote Commands:

#### Commands which provide voting capability


   !hostvote vote_subject
   
        vote_subject = string
        Sends a message to allow currently unofficial voting on subjects

    
## Utility Commands:

#### Various Commands which provide misc utility
!manual_reg

        Manually start registration for yourself in case of bot error, REMOVES ALL REGISTRATION ASSIGNED ROLLS


!diceroll amount_of_dice amount_of_sides

        Rolls an amount_of_dice die, each having amount_of_sides sides.
        amount_of_dice = integer
        amount_of_sides = integer
        
!randrange low_end high_end

        Returns a random integer between low_end and high_end
        low_end, high_end = integers

!idea

        generates random game idea using karl's game idea generation functions

    
!clear

        Clears all messages in a channel.
        manage messages permissions required!
        
!covid19

        Gets current global covid19 global statistics
![weather|weather_at] lat lon
        OR
![weather|weather_at] zipcode
 
        Returns weather at specific latitude and longitude or by US zipcode
        lat, lon, zipcode = integers
        
## Stock Commands:

#### Commands for paper trading and stock analysis
!evaluateportfolio period indicators
        
        period: period to evaluate indicators over, default 10, must be above 1: integer
        indicators: list of indicators to pass

!technicals stock time_period

        returns technical indicator info about a stock
        extra_indicators (optional): list, extra indicators to use besides SMA,EMA, and RSI, see https://www.alphavantage.co/documentation/

        time_period (optional): integer, the time period in days to evaluate indicators over, default 10, must be over 1
        stock: string
        
!paperbuy stock amt_of_money


        Used for trading fake money on stocks!
        stock = string, stock to buy
        amt_of_money = integer

!papersell stock amt_of_stock

        Sell fake stocks!
        stock = string, stock to sell
        amt_of_stock = integer, amount of stock to sell

!portfolio

        Shows you all stocks you currently hold with the paper trading functionality.
      
!balance

        Shows current server fake money balance.
        
!value

        Shows the value of the stocks you are holding

        
## Fun Commands:

#### Commands which have useless, albeit fun functionality

!value

        Shows the value of the stocks you are holding


!coinflip

        Flips a coin

!robohash message
        
        Hashes msg into robot image
        messsag = string
        
!getxkcd comic_num

        Gets an XKCD comic comic_num and returns various info about it.

        comic_num = integer
        
!dog
        
        Returns a random image of a dog

!cat
        
        Returns an image of a cat

## Image Commands:

#### Commands which do stuff with images

!get_face

        Returns a mashed up image of a human face

!quantize (img attachment) number

        Attach an image to the message.

        Number should be from 1-256

        Bot will post a new image with colors reduced to the number specified

!get_channel (img attachment)  channel

        Channel should be 'r','g',or 'b'

        Bot will post an image of the color channel specified from the attached image
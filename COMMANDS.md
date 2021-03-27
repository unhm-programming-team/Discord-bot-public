#Discord Bot Commands

* this document describes all current working commands
* omit brackets from parameters, strings with spaces require quotes
## Vote Commands:

#### Commands which provide voting capability

!hostvote "vote subject"


        """
        Sends a message to allow currently unofficial voting on subjects
        :param vote_subject: string which contains voting subject
        :return: message with cross and check emojis
        """
    * Hosts a vote, uses vote subject directly in vote message
    * responds once with a check and cross emoji to enable users to easily vote
    
## Utility Commands:

#### Various Commands which provide misc utility
!idea [seed]

        """
        generates random game idea using karl's game idea generation functions
        :param seed: optional, default -1, integer to seed random generation
        :return: random game idea
        """
        
        * returns a random game idea using karl miller random game idea generation functions

    

!covid19

        """
        Gets current global covid19 statistics 
        :return: current covid 19 statistics according to covid19api.com
        """
        
        * returns statistics on covid 19 infections

!weather_at [latitude] [longitude] or just [zipcode]
        
        aliases: !weather, !weatherat

        """
        Returns weather at specific latitude and longitude
        :param lat: latitude or zip code of location
        :param lon: longitude of location
        :return: weather at lat,lon
        """
    * returns a message containing weather for a specific latitude 
      and longitude or a specified zip code.
    
    * if a zip code is provided a longitude must not be provided  
    
    * returns the following conditions:
        * Short weather description
        * Temperature
        * "feels like" temperature
        * level of humidity
        
## Fun Commands:

#### Commands which have useless, albeit fun functionality

!coinflip

        """
        Flips a coin
        :return: result of coin flip
        """``

!getXKCD comic_number

        aliases: !xkcd

        """
        Gets an XKCD comic and returns info about it
        ;param comic_number: the number of the xkcd comic
        :return: XKCD comic link, title, alt-text, explanation, and image title
        """
        
        * returns an XKCD comic and various info about it

!dog

        """
        Returns a random image of a dog
        :return: image of a dog
        """
        * simply provides the link to a random image of a dog
      
!cat

        """
        Returns an image of a cat
        :return: image of cat
        """
        
        * provides the link to a random image of a cat
        

!robohash "string"

        """
        Hashes string into robot image
        :param content: string to hash
        :return: image of a robot
        """
        
        * uses string to generate an image of a robot
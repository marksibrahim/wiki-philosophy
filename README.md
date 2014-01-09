wikipedia-philosophy
====================
tldr; a simple script to count number of steps it takes to hit the Philosopy page from a random Wikipedia page.


The alt text of this xkcd: http://xkcd.com/903/ says:

"Wikipedia trivia: if you take any article, click on the first link in the article text not in parentheses or italics, and then repeat, you will eventually end up at "Philosophy"."

And sure enough, most do. There are some which end up in a few loop within themsevles and never get out. For example, http://en.wikipedia.org/wiki/Axis_powers and http://en.wikipedia.org/wiki/Allies_of_World_War_II  are in a two-page loop. Because of that, you can never reach Philosophy if you start with something like http://en.wikipedia.org/wiki/Bougainville_Campaign.

And there are others which link to non-existing pages, reaching a dead-end.

Still a large number of pages do eventually reach Philosophy. So this script starts with a random Wikipedia page and follows the first link until it gets to Philosophy and adds the number of steps it takes to reach there to the accompanying CSV file, then moving to get another random page.


Instructions
-----------
- It is a good idea to download the Wikipedia dump from http://dumps.wikimedia.org/ and try this locally. It works in the live Wiki site but is painfully slow.
- Change the variable 'attempts' to whatever number of sets of a-random-page-to-philosopgy trip you'd like to do.
- Change the variable 'limit' to whatever number of pages to hop before marking the current page as a failed page to reach philosophy.

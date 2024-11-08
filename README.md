# The Mansfield Flash

#### Video Demo: https://youtu.be/PwQFhP_PvqA

#### Description:

My issue was simple: I'm moving to Mansfield, TX soon and noticed a lack of news coverage. There is a small local paper, but it only produces content once a week and is very traditional. It doesn't produce a lot of the content that internet readers want to read. I figured that I could create a website that aggregates news for Mansfield and orders it in a way that is relevant.

The first thing I had to do was find the right stories to pull in and how to order them. Google News has a local section that they use, but it does not do a good job at ranking them in importance or in proximity to the city. It takes news of the general area and populates them in the list. I eventually wanted this to be a daily newsletter, so I made a decisions: 1.) I wanted the mosted relevant information to Mansfield first. 2.) I only wanted the most recent stories. 3.) I wanted to minimize computing time and also provide a list of stories that felt completable.

My original plan was to pull from a Google News API, but that didn't exist. Google removed that functionality years ago. I searched github and found a python package that helped me parse the feeds. From there, it was a matter of parsing the right feed (the one local to Mansfield, TX) and re-ordering the stories. Those that had Mansfield in the headline would be the most relevant, so I ranked those first. I also ranked any story written by the local paper first as well.

Once I created that, I built a HTML templage and index page using Jinja. I also used bootstrap and some custom styling to give the page a minimalist design while keeping it readable.

Being a former journalist, I knew weather is a popular thing people search for. I wanted real-time information to pull weather in. There were several APIs that would allow me to do that, but I chose to go with the weather.gov API. It was free, a government site, and had all the information I needed.

After pulling the data I imported it into my flask app and rearranged the index page to put in the placeholders. I had a working prototype but my initial design didn't feel professional enough.

I then used ChatGPT and Claude to make my design look better. At first I tried to pull images in, but that didn't work because the way I was pulling in stories didn't allow me to get images from the stories. It just showed the Google News image over and over. After tweaking prompts -- and reverting my code back -- I was able to figure out a nice alternative, but I do think it still needs some work. I would also like to find a way to have an event calendar. I know that is something people are seeking out and would be helpful for me as well. I am also working on moving this from my local device to an website as others in my neighborhood have run into the same problem as me when it came to finding relevant information.

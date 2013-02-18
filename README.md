lafitness
=========

Provides a Python wrapper for LA Fitness's customer portal (via web scraping)

Motivation
==========

I'm a member at LA Fitness (in Portland, OR).

I love the gym, but the online customer 'portal' absolutely sucks.

So this is me trying to fix it, by developing a sane data wrapper over it.

Usage
=====

from lafitness import LAFitness

la = LAFitness(username='YOUR_USERNAME', password='YOUR_PASSWORD')
print la.get_checkin_history()

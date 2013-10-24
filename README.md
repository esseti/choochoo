##CHOOCHOO
Choochoo is a home-made project that aims at simplifying the searching of trains on trenitalia websites (which owns the data).

So far it implements (and not so well) the searching of delays by stations (list is taken from the websiste and sometimes names collide with the service returing a *no data* output). 

###HOW IT WORKS
The websiste makes requests to `mobile.viaggiatreno.it` and parses the responses (which are plain, and badly generated, HTML pages).  That's it.

It would be terrific if someone starts to build APIs for that. 
This code can be partially reused for building APIs, if someone wants to start a side project fell free to contact me.

### 4 DEVELOPERS
If you want to use the code, you need to install `requests` and `crispy-forms` in a manual way, since app-engine does not support them natively.
The simplest way is to install them via pip and then create a symbolic link in the project main folder.   

### NOTE:
- all the data belong to trenitalia.
- this is not for profit, so if you (trenitalia) don't like it pls speak up before sue me :)
- the code is badly and partialy commented (sorry, i'll fix once i've time).
- most of the code names are in italian (or pseudo italian).

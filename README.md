# DNSWait

`dnswait` is a small script to wait for the "propagation" of a namserver configuration.


## There's no such thing as DNS propagation

What make your browser don't hit your server right after you've
configured the zone, this long frustrating delay from hours to days,
is the effect of `caches`, not "propagation".

Try it yourself next time you set up a new entry: just don't hit it
before configuring it, so its absence is not stored in any
caches. Only when configured try it and boom, cache miss all the way
up, no delay, it just works.

There may be some time though between the moment you ask your
registrar to set an entry (via their web user interface or their API)
and the moment it's really visible on their nameservers, that time I
agree to call "propagation", and that's what's being monitored by this
script.


## Usage

Say you've added a TXT record containing `itsme` to proove you're the
owner of `example.com`, via the interface of a low-cost hosting
company, and they display a nice message:

> Please wait a few minutes for our scripts to propagate the change to
> our DNS servers.

Then you can run:

    dnswait example.com TXT itsme

the script will wait for all the authoritative servers of example.com
to serve `itsme` for your text entry, so you know exactly what those
`few minutes` were, you don't have to guess.



## Another example

Say you're the owner of `mdk.fr` (it's me) and your provider only
allows you to change DNS records using issues on their `bug tracker`,
then submit the issue asking them to set 51.15.187.166 as the IP for
mdk.fr and run:

    dnswait mdk.fr A 51.15.187.166

so you'll know when they do it.


If they reply "it's done" while `dnswait` don't see it, they probably
messed up something...


## Using in shell scripts

If you have a shell script updating DNS configuration via an API, you
can use `dnswait` in them to wait for the configuration to be done.


## Verbose

If you want to see what's happening, run with `-v` or `-vv`:

```bash
$ dnswait mdk.fr A 51.15.187.166 -v
INFO:dnswait:3 authoritative name servers to check.
INFO:dnswait:All authoritative servers have the expected value.
```

or:

```bash
$ dnswait mdk.fr A 51.15.187.166 -vv
INFO:dnswait:3 authoritative name servers to check.
DEBUG:dnswait:Checking ns-69-a.gandi.net.
DEBUG:dnswait:ns-69-a.gandi.net. have the expected value!
DEBUG:dnswait:Checking ns-173-b.gandi.net.
DEBUG:dnswait:ns-173-b.gandi.net. have the expected value!
DEBUG:dnswait:Checking ns-127-c.gandi.net.
DEBUG:dnswait:ns-127-c.gandi.net. have the expected value!
INFO:dnswait:All authoritative servers have the expected value.
```

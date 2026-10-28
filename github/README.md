# Liber Primus - Comprehensive Analysis and Solving Attempts

## Overview
This repository is my dedicated effort to document the knowledge, analysis, and solving attempts of *Liber Primus*, the cryptographic book that emerged as part of the *Cicada 3301* puzzle series. It is structured to provide historical context, linguistic analysis, cryptographic techniques, and documented efforts to decipher its contents. 

- [ ] Rewrite README.md to be more comprehensive; more information, and more correct.

- [ ] Document ciphers -> ./references/ciphers/

- [ ] Add all used books -> ./references/books/ (either by linking due to length or text format)

- [ ] Document and create tools -> ./tools/ (includes any software that helped with the deciphering of any part of Cicada)

- [ ] Solve the Liber Primus.

## Introduction

<details>
  <summary>Background || What Is Cicada?</summary> <br>
**Cicada 3301** is an enigmatic organization that first appeared online in 2012, posting a cryptic message on forums such as 4chan. The message invited individuals to solve a series of puzzles, suggesting that they were seeking highly intelligent individuals. Over time, Cicada 3301 gained a reputation as one of the most sophisticated and mysterious internet puzzles, incorporating elements from cryptography, steganography, classical literature, philosophy, and various coding techniques. While no group has ever definitively claimed responsibility for Cicada 3301, speculation abounds, with theories ranging from it being a recruitment tool for intelligence agencies to an independent secret society aiming to promote privacy, cryptography, and free information.
</details>

<details>
  <summary>Background || 2012 & 2013</summary>
<h2>2012</h2>

On January 4, 2012, a [mysterious image](https://static.wikia.nocookie.net/uncovering-cicada/images/2/21/Final.jpg_2012.jpg/revision/latest?cb=20140110060301) appeared on 4chan's /x/ and /b/ boards, displaying the following message:

> *"Hello. We are looking for highly intelligent individuals. To find them, we have devised a test. There is a message hidden in this image. Find it, and it will lead you on the road to finding us. We look forward to meeting the few that will make it all the way through. Good luck. 3301"*

Users soon discovered that analyzing the image's raw data via a text editor revealed a hidden text string:

> "TIBERIVS CLAVDIVS CAESAR says 'lxxt>33m2mqkyv2gsq3q=w]O2ntk'."

Recognizing the reference to Emperor Tiberius Claudius Caesar, solvers quickly identified it as a Caesar cipher. Deciphering it led to a URL, which contained [another image](https://i.imgur.com/m9sYK.jpg).

Using steganography software OutGuess, solvers extracted a hidden message:

> "Here is a book code. To find the book, and more information, go to http://www.reddit.com/r/a2e7j6ic78h0j/."

The subreddit contained cryptographic messages, signed using PGP keys, confirming authenticity. The messages included references to King Arthur and The Mabinogion, a medieval Welsh text. Through decryption, users uncovered a book cipher, instructing them to extract letters from specific lines in a text, leading to a phone number. Calling the number played a voice message instructing callers to find two more prime numbers related to the original image and multiply them with 3301. The dimensions of the image, 509x503 pixels, were both prime numbers. Multiplying *509 × 503 × 3301* resulted in 845145127, which, when appended with ".com," led to a new website (845145127.com), featuring a countdown timer. When the countdown expired, the site updated with a list of global coordinates.

These coordinates pointed to physical locations worldwide, including Paris, Warsaw, Miami, Seoul, and Sydney. Participants visiting these locations found posters featuring QR codes and a cicada emblem. Scanning the QR codes revealed Tor (.onion) URLs, leading to more encrypted messages. Two specific texts—*Agrippa: A Book of the Dead* and* Encyclopædia Britannica*—were referenced, each requiring book cipher decryption to retrieve new onion addresses.

Upon accessing these .onion links, solvers were prompted to submit an email. Those who complied received a unique RSA-encrypted message along with a public key. Participants were warned against sharing their keys, as doing so resulted in disqualification. The task was to factorize the RSA modulus into two prime numbers to decrypt the message. The modulus, intentionally small, made factorization possible using software like *factmsieve.py*. Successfully decrypting the message led to another hidden service URL. Participants who reached this stage received an encrypted MIDI file. The file contained two musical tracks, which, when analyzed, were found to encode text. Each note and duration represented a letter. The first track was a substitution cipher encoding a passage from *William Blake's "A Song of Liberty"*, while the second track provided a shifted version of the cipher key. Using this information, solvers extracted a final set of instructions.

The instructions required solvers to generate a GPG key linked to their email, upload it to MIT's PGP keyserver, encrypt a specific list of words, and email it back. The word list included seemingly random terms such as "muscle, drop, pump, knee, bird, watch, bell," and so on. Only those who followed these steps correctly received final login credentials to a hidden Tor site. And just like that, the first puzzle concluded.

A month later, a farewell message, cryptographically signed by 3301, was posted on the original subreddit. No further verified messages were received that year, and the puzzle ended with no public explanation of its purpose.

<h2>2013</h2>

On **January 4, 2013**, a year after the first puzzle, a new Cicada 3301 image appeared on 4chan, with similar cryptographic elements. Users once again extracted hidden text using OutGuess, revealing a message that directed them to a new subreddit. The subreddit contained PGP-signed messages and cryptographic challenges, continuing the themes from the previous year.

> *"Hello again. Our search for intelligent individuals now continues. The first clue is hidden within this image. Find it, and it will lead you on the road to finding us. We look forward to meeting the few that will make it all the way through. Good luck. 3301"*

Solvers decrypted a book cipher, leading to an obscure piece of literature. Further decryption revealed a phone number that, when called, played a pre-recorded message instructing solvers to find and use three prime numbers associated with the image. These numbers, when multiplied, formed a new URL leading to an updated Cicada website with another countdown timer. Once expired, the website provided a new set of global coordinates. Individuals who visited these locations found QR codes on posters featuring Cicada’s emblem. Scanning these QR codes revealed hidden .onion links, directing solvers to additional challenges. This phase included advanced cryptographic puzzles, including RSA decryption and book ciphers referencing texts like *Liber AL vel Legis* and *The Book of the Law*.

Those who decrypted the messages were instructed to submit an email, after which they received unique RSA-encrypted messages. Participants were explicitly warned against sharing their information, as doing so would result in removal from the puzzle. Decrypting the RSA key required factoring large prime numbers. Successfully doing so granted access to yet another Tor-based hidden service.

Unlike the first puzzle, this one never concluded with an official message from Cicada. The trail merely went cold, and amateur solvers were left only to debate about the real purpose of these puzzles.
</details>

<details>
  <summary>Background || 2014 - Liber Primus</summary> <br>

On **January 5, 2014**, a year after the second puzzle, once more, Cicada 3301 reentered the internet space with the beginning to another puzzle, this time with a message far more cryptic than any other one we've seen so far.

> *"Hello. Epiphany is upon you. Your pilgrimage has begun. Enlightenment awaits. Good luck. 3301*

The process remains true to the previous puzzles. The image contained hidden text, the text led to a book, and gradually the puzzle unfolded. Except this time, the puzzle seemed to have hit a breaking point with the book part. The book was called *Liber Primus*, and was supposedly written by Cicada. Through several .onion links, all pages of the book were all uncovered. And this is where we stand today...
</details>

---

This repository serves as a centralized self-resource for:
- The history and background of *Liber Primus*.
- Documented decryption attempts and successful translations.
- Cryptographic methodologies applied to decoding the book.
- Theories regarding its purpose and underlying messages.
- Tools and scripts designed to facilitate analysis.

## Repository Structuring
```
/                     # Root directory
│ ─ research/         # Historical context, interpretations, and academic insights
│ ─ solutions/        # Documented decryption attempts and verified translations
│ ─ tools/            # Scripts and programs for cipher analysis and decryption
│ ─ references/       # Links, books, papers, and additional resources
│ ─ README.md         # This document
```

## Additional Resources
For further research and collaboration, the following resource(s) may be useful:
- [Cicada 3301 Wiki](https://uncovering-cicada.fandom.com/wiki/Uncovering_Cicada_Wiki)

## Disclaimer
This repository is intended for educational and analytical purposes. It is not affiliated with *Cicada 3301* or any related entities. The contents of *Liber Primus* remain largely speculative, and interpretations provided here are based on collective research efforts.

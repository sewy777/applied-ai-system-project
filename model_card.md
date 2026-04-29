# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 2.0**

---

## 2. Intended Use  

VibeFinder 1.0 is designed to suggest songs from a small catalog based on a user's stated genre, mood, and energy preferences. It's meant for classroom exploration — specifically to show how a basic content-based recommender works from the inside. It assumes the user already knows what genre and mood they're in the mood for, which isn't always realistic.

**Not intended for:** real production use, real users with complex or changing tastes, or any situation where fairness or diversity across genres actually matters. It also shouldn't be used as a substitute for a proper music recommendation engine — the catalog is tiny and the scoring logic is intentionally simplified.

---

## 3. How the Model Works  

You give the system three things: your favorite genre, your current mood, and how energetic you want the music to feel (on a scale of 0 to 1). The system then goes through every song in the catalog and gives each one a score based on how well it matches what you said.

Here's how the points work: if a song's genre matches yours, it gets 2 points. If the mood matches, it gets 1 point. Then there's a small bonus — up to 1 extra point — based on how close the song's energy level is to what you asked for. The closer it is, the higher the bonus. Once every song has a score, the system sorts the list from highest to lowest and hands you the top 5.

That's basically it. No machine learning, no training data — just math on a spreadsheet of songs.

---

## 4. Data  

The catalog has 18 songs total. The original starter file had 10, and I added 8 more to cover genres that were missing. Each song has 9 attributes: id, title, artist, genre, mood, energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), and acousticness (0–1).

Genres covered: pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, edm, r&b, metal, classical, hip-hop, folk, reggae. That's 15 different genres for 18 songs, so most genres only have one representative track. Moods covered include happy, chill, intense, relaxed, moody, focused, nostalgic, euphoric, romantic, peaceful, confident, melancholic, and laid-back.

The biggest gap is that the dataset reflects a pretty specific slice of musical taste — mostly English-language Western genres. There's nothing representing Latin music, K-pop, Afrobeats, or anything outside that space. It also doesn't capture things like lyrics, tempo changes within a song, or how a song makes you feel over time.

---

## 5. Strengths  

The system works best when the user's genre is well-represented in the catalog. For example, the Chill Lofi profile got three strong genre matches right away, and all three felt genuinely right — quiet, slow, study-friendly tracks. The Deep Intense Rock profile also nailed it: Storm Runner came up first with a near-perfect score because it matched genre, mood, and energy all at once.

The other big strength is transparency. Unlike a black-box AI, you can see exactly why every song was recommended — the output tells you "genre match (+2.0), mood match (+1.0), energy similarity (+0.97)" right there in the terminal. That's actually something real streaming apps don't always give you, and it makes it really easy to debug or adjust the logic.

---

## 6. Limitations and Bias 

The biggest weakness I noticed is that genre has way too much influence over everything else. Because a genre match is worth +2.0 points and a mood match is only +1.0, a song that perfectly matches your mood and energy but is in a slightly different genre will almost always lose to a genre match — even if the genre match feels totally wrong. For example, "Gym Hero" (an intense pop workout song) kept showing up in the top 2 for the High-Energy Pop profile even though the user wanted happy vibes, not intense ones. The system just saw "pop" and gave it 2 points regardless. Another thing I found is that when someone asks for a genre with very few songs in the catalog (like classical or rock, which only has one song each), the system quickly runs out of real matches and starts recommending songs purely based on energy similarity, which means a metal song might show up for a classical music fan just because both are around the same tempo. The energy similarity score also maxes out at +1.0 which is too small to overcome the genre bonus — so it never really acts as a tiebreaker the way it's supposed to.

---

## 7. Evaluation  

I tested five different user profiles to see how the recommender behaved across different music tastes. The three main ones were High-Energy Pop, Chill Lofi, and Deep Intense Rock — basically covering opposite ends of the energy and genre spectrum. Then I added two adversarial profiles to stress-test the system: a "High-Energy Classical" user (classical music is usually calm, so asking for high energy + classical creates a conflict) and a "Sad EDM" user (our only EDM song is tagged as euphoric, not sad).

The results for the normal profiles made a lot of sense — Chill Lofi surfaced Library Rain and Midnight Coding right away, and Deep Intense Rock correctly put Storm Runner at the top with a near-perfect score. What surprised me though was the adversarial results. The High-Energy Classical profile still ranked Morning Mist first (score 2.27) even though it's a very calm, peaceful song — just because it was the only classical track in the catalog. The system gave it +2.0 for genre and then penalized it for the energy mismatch, but that 2.0 head start was enough to beat everything else. The second pick was actually Bass Drop Heaven (EDM) because it matched the "euphoric" mood and had high energy, which honestly felt more right for what the user was describing.

I also ran a weight shift experiment: I halved the genre weight (+2.0 → +1.0) and doubled the energy similarity weight. The rankings shifted noticeably in the middle — songs that were close in energy but wrong genre moved up, and mood matches became more competitive. The top spot didn't change (because the best song still matched everything), but the gap between 2nd and 3rd place narrowed significantly. This told me the original weights are probably a bit too genre-heavy.

---

## 8. Future Work  

1. **Balance the weights.** Genre is currently worth twice as much as mood, which makes it feel like a hard filter. I'd experiment with making all three factors — genre, mood, and energy — more equal so a great mood + energy match can actually compete with a genre match.

2. **Add a diversity rule.** Right now the same artist or genre can show up multiple times in the top 5. I'd add a penalty so the system doesn't recommend two songs from the same artist back to back — that would make the list feel more like a real playlist.

3. **Grow the catalog and add collaborative signals.** 18 songs is way too small for real use. Adding more songs per genre would fix the sparsity problem immediately. Longer term, tracking which songs users actually skip or replay would let you mix in some collaborative filtering on top of the content-based scoring.

---

## 9. Reflection and Ethics

**What are the limitations or biases in your system?**

The biggest problem is that genre basically runs everything. Genre gives +2.0 points, mood only gives +1.0, so a song that perfectly matches your mood and energy but is the wrong genre will almost always lose. I noticed this with the "Gym Hero" track — it kept showing up near the top of the High-Energy Pop list even though it's tagged as "intense," not "happy," just because it's pop. Also the catalog only has 18 songs, so if you pick a genre with one track (like classical or metal), the system runs out of real options really fast and just starts picking things based on energy alone. It can't tell you "I don't have anything great for you" — it just hands you whatever's closest, even if it's not close at all.

**Could your AI be misused, and how would you prevent that?**

Honestly, in this form it's pretty low-risk — it's just recommending songs from a tiny fixed catalog. But the same logic at a bigger scale could create a filter bubble problem. If genre is always worth double, users who like pop will basically only ever see pop, forever. They'd never discover anything outside their comfort zone. To fix that I'd add a diversity rule — something like "no more than 2 songs from the same genre in the top 5" — and maybe introduce a small random factor so the results aren't totally locked in every time. The input validation I added is also important — without it, if someone passes a broken energy value the system would just silently give bad results.

**What surprised you while testing your AI's reliability?**

I expected the confidence scores to be more spread out, but almost every well-matched profile came back at 99%+. At first I thought that meant the system was really good, but then I realized it just means genre is doing basically all the work — once a genre match happens, the score jumps so high that mood and energy barely matter. The other thing that surprised me was how useful the guardrail tests were. I hadn't thought about what happens when someone passes an energy value above 1.0 until I actually sat down to write a test for it. Testing made me think about failure cases I would have completely missed otherwise.

**Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.**

I used AI help throughout this project. One thing that was genuinely useful was the suggestion to raise a specific `ValueError` message for each type of bad input in `validate_user_prefs` — like separately handling missing genre, missing mood, and out-of-range energy. That made the guardrails a lot more useful when something actually went wrong because the error told you exactly what the problem was. One thing that was wrong though was an early version of the confidence calculation that divided the score by the highest score in the current results instead of the fixed maximum (4.0). That would have meant the top song always showed 100% confidence no matter how bad the match was, which defeats the whole purpose. I had to think it through myself to realize why that was wrong and switch it to use the theoretical maximum instead.

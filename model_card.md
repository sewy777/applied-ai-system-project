# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

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

The biggest limitation is that genre dominates every result. Because a genre match gives +2.0 points and a mood match only gives +1.0, the system basically treats genre as a hard filter — a song that perfectly matches your mood and energy but is in a slightly different genre will almost always lose. The catalog is also only 18 songs, so genres with just one track (like classical or metal) have almost no real competition. The system also doesn't understand what a song actually sounds like — it only sees labels and numbers, so it has no way to catch cases where the label is wrong or misleading.

**Could your AI be misused, and how would you prevent that?**

In its current form the system is low-risk — it's just song recommendations from a small fixed catalog. But the same design pattern scales up, and at scale, a genre-heavy recommender could create filter bubbles: a user who likes pop gets only pop forever, which pushes them away from discovering anything new. To prevent this, you'd add a diversity rule (no more than 2 songs from the same genre in the top 5) and mix in some randomness or exploration. The input validation added in this version is also a basic safeguard — it rejects bad inputs early rather than silently producing wrong results.

**What surprised you while testing your AI's reliability?**

The confidence scores were almost all above 99% for well-matched profiles, which I didn't expect. I thought there would be more spread. It showed me that when genre matches, the system is basically certain — and when it doesn't, the score drops sharply. The guardrail tests were also useful because I hadn't thought carefully about what happens when someone passes an energy value above 1.0 until I actually wrote the test for it. Testing found edge cases I hadn't considered.

**Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.**

I used AI assistance throughout this project. One helpful suggestion was the structure of the `validate_user_prefs` function — the AI suggested raising a `ValueError` with a specific message for each bad input rather than a generic error, which made the guardrails much clearer and easier to debug. One suggestion that was flawed was an early version of the confidence calculation that divided by the top score in the current results instead of the theoretical maximum (4.0). That would have made confidence relative to the best result in each run, so the top song would always show 100% regardless of how poor the match actually was. I caught it by thinking through what the number was supposed to mean and fixed it to use the fixed maximum instead.

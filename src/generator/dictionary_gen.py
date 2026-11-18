# src/generator/dictionary_gen.py
import random
from typing import Optional, List, Dict
from src.generator.base import BaseGenerator, DiscordRuleValidator

CONSONANTS = "bcdfghjklmnprstvwz"
VOWELS = "aeiou"
DIGITS = "0123456789"

# Curated high-value English words by length
POPULAR_3LETTER_WORDS: List[str] = [
    "ace", "act", "air", "ale", "all", "amp", "ant", "ape", "arc", "arm", "art", "ash", "ask", "axe",
    "bad", "bag", "bar", "bat", "bay", "bed", "bee", "beg", "bet", "bid", "big", "bin", "bit", "bow",
    "box", "boy", "bug", "bus", "buy", "cab", "can", "cap", "car", "cat", "cop", "cow", "cry", "cup",
    "cut", "dad", "dam", "day", "den", "dew", "die", "dig", "dim", "dog", "dot", "dry", "due", "ear",
    "eat", "egg", "ego", "elf", "elm", "end", "era", "eve", "eye", "fan", "far", "fat", "fed", "fee",
    "few", "fig", "fin", "fit", "fix", "fly", "foe", "fog", "for", "fox", "fun", "fur", "gap", "gas",
    "gem", "get", "gin", "god", "gum", "gun", "guy", "gym", "hat", "hay", "hen", "hex", "hid", "hip",
    "hit", "hop", "hot", "hub", "hug", "hum", "hut", "ice", "ill", "ink", "inn", "ion", "ivy", "jam",
    "jar", "jaw", "jay", "jet", "job", "jog", "joy", "jug", "key", "kid", "kin", "kit", "lab", "lad",
    "lap", "law", "lay", "leg", "lid", "lie", "lip", "lit", "log", "lot", "low", "mad", "man", "map",
    "mat", "max", "may", "men", "met", "mix", "mob", "mom", "mud", "mug", "net", "new", "nil", "nod",
    "nor", "not", "now", "nut", "oak", "oar", "oat", "odd", "off", "oil", "old", "one", "opt", "orb",
    "ore", "our", "out", "owl", "own", "pad", "pan", "pat", "paw", "pay", "pea", "peg", "pen", "pet",
    "pie", "pig", "pin", "pit", "ply", "pod", "pop", "pot", "pro", "pub", "pun", "pup", "raw", "ray",
    "red", "rib", "rid", "rim", "rip", "rob", "rod", "row", "rub", "rug", "rum", "run", "rut", "rye",
    "sad", "sag", "sap", "sat", "saw", "sea", "see", "set", "sew", "she", "shy", "sin", "sip", "sir",
    "sit", "six", "ski", "sky", "sly", "sob", "son", "sow", "soy", "spa", "spy", "sub", "sue", "sum",
    "sun", "tab", "tag", "tan", "tap", "tar", "tea", "ten", "the", "thy", "tie", "tin", "tip", "toe",
    "ton", "top", "tow", "toy", "try", "tub", "tug", "two", "urn", "use", "van", "vat", "vet", "vex",
    "via", "vim", "vow", "war", "wax", "way", "web", "wet", "who", "why", "wig", "win", "wit", "woe",
    "won", "yak", "yam", "yap", "yaw", "yea", "yen", "yes", "yet", "yew", "yin", "zap", "zed", "zen",
    "zig", "zip", "zoo"
]

POPULAR_4LETTER_WORDS: List[str] = [
    "acid", "apex", "arch", "atom", "aura", "auto", "axis", "baby", "bake", "bald", "band", "bark",
    "base", "beam", "bean", "bear", "beat", "beef", "beer", "bell", "belt", "best", "bird", "bite",
    "blow", "blue", "boat", "body", "bold", "bomb", "bone", "book", "boom", "boot", "boss", "bowl",
    "bull", "burn", "bush", "busy", "cage", "cake", "calm", "camp", "cape", "card", "care", "cart",
    "case", "cash", "cast", "cave", "cell", "chat", "chef", "city", "clap", "claw", "clay", "clip",
    "club", "clue", "coal", "coat", "code", "coin", "cold", "cook", "cool", "copy", "core", "corn",
    "cost", "crab", "crew", "crop", "cube", "cure", "curl", "cute", "dark", "dawn", "dead", "deal",
    "dear", "deck", "deep", "deer", "desk", "diet", "dirt", "disc", "dock", "dome", "door", "dose",
    "dove", "down", "drag", "draw", "drop", "drum", "duck", "dust", "duty", "earn", "east", "echo",
    "edge", "epic", "evil", "exit", "face", "fact", "fade", "fail", "fair", "fall", "fame", "farm",
    "fast", "fate", "fear", "feat", "feed", "feel", "fern", "film", "find", "fire", "fish", "fist",
    "flag", "flat", "flew", "flex", "flip", "flow", "foam", "fold", "font", "food", "fool", "fork",
    "form", "fort", "foul", "free", "frog", "fuel", "fury", "fuse", "game", "gang", "gate", "gear",
    "geek", "gift", "girl", "glow", "glue", "goat", "gold", "golf", "good", "grab", "gray", "grid",
    "grim", "grip", "grit", "grow", "gulf", "gust", "guru", "hail", "hair", "half", "halo", "halt",
    "hand", "hang", "hard", "harm", "hate", "hawk", "head", "heal", "heat", "heel", "help", "herb",
    "herd", "hero", "hide", "high", "hill", "hint", "hold", "hole", "holy", "home", "hood", "hook",
    "hope", "horn", "hose", "host", "hour", "hunt", "hurt", "hush", "hype", "icon", "idea", "idle",
    "idol", "inch", "iron", "item", "jail", "jazz", "jeep", "join", "joke", "jump", "junk", "jury",
    "keen", "keep", "kick", "kill", "kind", "king", "kiss", "kite", "knee", "knit", "knot", "lace",
    "lack", "lady", "lake", "lamb", "lamp", "land", "lane", "last", "late", "lava", "lawn", "lead",
    "leaf", "lean", "leap", "left", "lens", "life", "lift", "like", "lime", "line", "link", "lion",
    "list", "live", "load", "loan", "lock", "loft", "logo", "long", "look", "loop", "lord", "lore",
    "loss", "loud", "love", "luck", "luna", "lure", "lush", "lute", "lynx", "mace", "made", "mage",
    "mail", "main", "make", "many", "mark", "mask", "mass", "mast", "mate", "maze", "meal", "mean",
    "meat", "mega", "melt", "memo", "mesh", "mess", "mile", "milk", "mill", "mind", "mine", "mint",
    "miss", "mist", "mode", "mold", "mole", "monk", "mood", "moon", "moss", "moth", "move", "much",
    "myth", "nail", "name", "navy", "near", "neat", "neck", "neon", "nest", "news", "next", "nice",
    "node", "noir", "noon", "norm", "nose", "note", "nova", "nude", "nuke", "null", "oath", "ocean",
    "odor", "omen", "once", "only", "onyx", "open", "orca", "oven", "over", "pack", "page", "pain",
    "pair", "pale", "palm", "park", "part", "pass", "past", "path", "peak", "peel", "peer", "pike",
    "pile", "pine", "pink", "pipe", "plan", "play", "plot", "plug", "poem", "poet", "pole", "pond",
    "pool", "pork", "port", "pose", "post", "pour", "pray", "pure", "push", "quiz", "race", "rage",
    "raid", "rail", "rain", "rank", "rare", "rate", "rave", "rays", "read", "real", "reap", "rear",
    "redo", "reed", "reef", "reid", "rein", "rely", "rest", "rice", "rich", "ride", "rift", "ring",
    "riot", "ripe", "rise", "risk", "road", "roam", "roar", "robe", "rock", "role", "roof", "room",
    "root", "rope", "rose", "ruby", "ruin", "rule", "rune", "rush", "rust", "safe", "sage", "sail",
    "salt", "sand", "save", "scan", "scat", "seal", "seam", "seed", "seek", "seem", "self", "send",
    "serf", "shad", "shin", "ship", "shoe", "shop", "shot", "show", "shut", "sick", "side", "sigh",
    "sign", "silk", "sine", "sing", "sink", "sire", "site", "size", "skip", "skit", "slab", "slam",
    "slap", "slot", "slow", "slug", "snap", "snow", "soak", "soap", "soar", "sock", "sofa", "soil",
    "sole", "solo", "song", "soon", "soul", "soup", "sour", "span", "spin", "spit", "spot", "star",
    "stay", "step", "stew", "stop", "suit", "surf", "swan", "swim", "tail", "take", "tale", "talk",
    "tall", "tank", "tape", "task", "team", "tear", "tech", "tell", "tent", "term", "test", "text",
    "tide", "tile", "time", "tiny", "tire", "toad", "toll", "tomb", "tone", "tool", "toon", "tour",
    "town", "trap", "tray", "tree", "trek", "trim", "trio", "trip", "true", "tube", "tune", "turn",
    "twin", "type", "ugly", "unit", "upon", "urge", "user", "vail", "vain", "vale", "vamp", "vane",
    "vary", "vase", "vast", "veil", "vein", "vent", "verb", "vest", "vibe", "vice", "view", "vine",
    "visa", "vise", "void", "volt", "vote", "vow", "wade", "wage", "wail", "wait", "wake", "walk",
    "wall", "wand", "ward", "warm", "warn", "warp", "wary", "wash", "wasp", "wave", "weak", "wear",
    "weed", "week", "weep", "west", "wild", "wind", "wine", "wing", "wire", "wise", "wish", "wolf",
    "wood", "wool", "word", "work", "worm", "wrap", "yard", "yarn", "year", "yoga", "yolk", "zeal",
    "zero", "zinc", "zone", "zoom"
]

POPULAR_5LETTER_WORDS: List[str] = [
    "apple", "about", "above", "acute", "admit", "adopt", "agent", "agile", "ahead", "alarm", "album",
    "alert", "alien", "align", "alive", "alpha", "alter", "amber", "among", "angel", "angle", "anime",
    "apron", "arena", "armor", "arrow", "aside", "asset", "audio", "audit", "axiom", "azure", "bacon",
    "badge", "badly", "basic", "beach", "begin", "beige", "bench", "berry", "birth", "black", "blade",
    "blank", "blast", "blend", "bless", "blind", "blink", "block", "bloom", "blown", "board", "boost",
    "bonus", "bound", "brain", "brand", "brave", "bread", "break", "brick", "brief", "broad", "brook",
    "brown", "brush", "build", "buyer", "cabin", "cable", "camel", "candy", "cargo", "carry", "catch",
    "cause", "chain", "chair", "chalk", "charm", "chart", "chase", "cheap", "check", "chess", "chief",
    "child", "chill", "china", "chunk", "civic", "civil", "claim", "clash", "clean", "clear", "clerk",
    "cliff", "climb", "clock", "clone", "close", "cloth", "cloud", "clown", "coach", "coast", "coral",
    "craft", "crash", "crawl", "crazy", "cream", "creed", "creek", "crest", "crime", "crisp", "crown",
    "crush", "cyber", "cycle", "daily", "dance", "datum", "debut", "decay", "delay", "delta", "demon",
    "dense", "depot", "depth", "devil", "diary", "digit", "diner", "dirty", "disco", "diver", "dizzy",
    "donor", "doubt", "draft", "drain", "drama", "dream", "drift", "drink", "drive", "drown", "eagle",
    "early", "earth", "eight", "elbow", "elder", "elite", "empty", "enemy", "entry", "equal", "error",
    "event", "every", "exact", "exile", "exist", "extra", "fable", "faith", "false", "fancy", "fatal",
    "fault", "feast", "fence", "fever", "fiber", "field", "fiery", "fifth", "fight", "final", "first",
    "flame", "flare", "flash", "fleet", "flesh", "float", "flock", "flood", "floor", "flora", "flour",
    "fluid", "flush", "flute", "focal", "focus", "force", "forge", "forth", "forum", "found", "frame",
    "frank", "fresh", "front", "frost", "fruit", "gamma", "gauge", "gecko", "ghost", "giant", "glide",
    "globe", "glory", "glyph", "grace", "grade", "grain", "grand", "grant", "graph", "grasp", "grass",
    "grave", "great", "green", "greet", "grief", "grill", "grind", "groove", "group", "guard", "guess",
    "guide", "habit", "happy", "haven", "heart", "heavy", "hedge", "hello", "honor", "hotel", "hound",
    "house", "human", "humid", "humor", "hyper", "ideal", "image", "index", "inert", "input", "irony",
    "issue", "ivory", "jeans", "jelly", "jewel", "joint", "joker", "judge", "juice", "jumbo", "karma",
    "kayak", "kebab", "knife", "knock", "koala", "label", "labor", "laser", "layer", "lemon", "level",
    "lever", "light", "limit", "linen", "links", "liver", "lobby", "logic", "lover", "loyal", "lucky",
    "lunar", "lunch", "magic", "major", "maker", "mango", "manor", "maple", "march", "mason", "match",
    "maxim", "mayor", "media", "melon", "mercy", "merge", "metal", "meter", "micro", "midst", "might",
    "miner", "minor", "minus", "model", "modem", "money", "month", "moral", "motor", "mount", "mouse",
    "movie", "music", "naive", "naval", "nerve", "never", "night", "ninja", "noble", "noise", "north",
    "novel", "nurse", "oasis", "ocean", "olive", "omega", "onion", "onset", "opera", "orbit", "order",
    "organ", "other", "ounce", "outer", "oxide", "ozone", "pager", "paint", "panel", "panic", "paper",
    "pasta", "patch", "pause", "peace", "peach", "pearl", "pedal", "penny", "phase", "phone", "photo",
    "piano", "piece", "pilot", "pinch", "piper", "pitch", "pivot", "pixel", "pizza", "place", "plain",
    "plane", "plant", "plate", "plaza", "point", "polar", "polka", "pound", "power", "press", "price",
    "pride", "prime", "print", "prior", "prism", "prize", "probe", "promo", "pulse", "punch", "pupil",
    "puppy", "puree", "purse", "queen", "query", "quest", "quick", "quiet", "quota", "quote", "radar",
    "radio", "raise", "rally", "ranch", "range", "rapid", "raven", "reach", "react", "realm", "rebel",
    "relic", "renew", "reset", "resin", "retro", "rhino", "rider", "ridge", "rifle", "right", "rigid",
    "risky", "rival", "river", "robot", "rocket", "rodeo", "rogue", "roman", "round", "route", "royal",
    "rugby", "ruler", "rumor", "rural", "saint", "salad", "salon", "salsa", "sauce", "scale", "scare",
    "scene", "scent", "scout", "scrap", "sense", "serum", "setup", "shade", "shake", "shark", "sharp",
    "sheep", "sheer", "sheet", "shelf", "shell", "shift", "shine", "shiny", "shock", "shoot", "shore",
    "short", "sight", "sigma", "silva", "silver", "simple", "since", "siren", "skill", "skirt", "skull",
    "slate", "sleep", "slice", "slide", "slope", "smart", "smell", "smile", "smoke", "snack", "snake",
    "solar", "solid", "solve", "sonic", "sound", "south", "space", "spark", "speak", "speed", "spice",
    "spicy", "spike", "spine", "spite", "spoon", "sport", "spray", "squad", "stage", "stair", "stake",
    "stand", "stark", "start", "state", "steam", "steel", "steep", "steer", "stick", "still", "stock",
    "stone", "storm", "story", "straw", "strip", "sugar", "suite", "super", "surge", "sweet", "swift",
    "sword", "table", "taste", "tiger", "titan", "token", "topic", "total", "toxic", "trace", "track",
    "trail", "train", "trend", "trial", "tribe", "trick", "ultra", "uncle", "union", "unity", "urban",
    "usage", "usher", "valid", "value", "valve", "vapor", "vault", "venue", "verse", "vessel", "video",
    "vigil", "vigor", "viper", "viral", "virus", "vital", "vivid", "vocal", "voice", "voter", "wagon",
    "waste", "watch", "water", "whale", "wheat", "wheel", "white", "whole", "widow", "width", "witch",
    "world", "worry", "worth", "wound", "wrist", "yacht", "yield", "young", "youth", "zebra"
]

POPULAR_6LETTER_WORDS: List[str] = [
    "action", "alpine", "animal", "anthem", "arcade", "artist", "aspect", "autumn", "avatar", "ballet",
    "banner", "beacon", "beauty", "beyond", "bishop", "blades", "blonde", "breeze", "bridge", "bronze",
    "bubble", "bullet", "bundle", "butter", "camera", "canvas", "carbon", "castle", "casual", "center",
    "chance", "change", "charge", "cherry", "cinema", "circle", "clarity", "clever", "client", "clover",
    "coffee", "column", "combat", "common", "copper", "corner", "cosmic", "cotton", "course", "cradle",
    "crater", "credit", "cricket", "crisis", "cruise", "crystal", "cursor", "damage", "danger", "dazzle",
    "decade", "degree", "delete", "demand", "deputy", "desert", "design", "desire", "detail", "device",
    "diesel", "digest", "dinner", "direct", "divert", "doctor", "domain", "dragon", "drawer", "driver",
    "dynamo", "eagles", "empire", "energy", "engine", "escape", "estate", "ethics", "exceed", "expert",
    "falcon", "family", "father", "fellow", "filter", "finger", "flavor", "flight", "flower", "flying",
    "forest", "fossil", "freeze", "friend", "fusion", "future", "galaxy", "gamble", "garden", "gentle",
    "glance", "glider", "golden", "guitar", "harbor", "hazard", "header", "heaven", "helmet", "hidden",
    "hollow", "honest", "hunter", "impact", "import", "island", "jacket", "jungle", "knight", "ladder",
    "legend", "liquid", "magnet", "market", "marvel", "matrix", "memory", "meteor", "mirror", "monkey",
    "mosaic", "motion", "muscle", "museum", "nation", "nature", "nebula", "nectar", "neural", "nickel",
    "notice", "octave", "office", "origin", "palace", "parade", "parrot", "patrol", "pepper", "phantom",
    "phoenix", "pioneer", "planet", "plasma", "portal", "poster", "powder", "prefix", "prince", "prison",
    "profit", "puzzle", "quantum", "rabbit", "radius", "random", "ranger", "rebel", "record", "region",
    "remedy", "rescue", "rhythm", "ribbon", "riddle", "ripple", "rocket", "runner", "safari", "sailor",
    "sample", "scalar", "scenic", "season", "second", "secret", "sensor", "serene", "shadow", "shield",
    "signal", "silent", "silver", "sketch", "smooth", "socket", "source", "spiral", "spirit", "splash",
    "spring", "square", "status", "stream", "strike", "studio", "summit", "sunset", "symbol", "target",
    "temple", "timber", "titan", "torque", "tracer", "travel", "tunnel", "update", "valley", "velvet",
    "vector", "vision", "voyage", "walnut", "weapon", "whisper", "wizard", "zenith", "zodiac"
]

class DictionaryGenerator(BaseGenerator):
    """
    Curated Dictionary & Phonetic Generator for lengths 3, 4, 5, 6.
    Generates meaningful English words, readable syllables, and alphanumeric variations.
    """
    def __init__(self, length: int = 4, exclude_reserved: bool = True):
        self.length = length
        self.exclude_reserved = exclude_reserved
        self._load_words()

    def _load_words(self):
        if self.length == 3:
            self.wordlist = POPULAR_3LETTER_WORDS
        elif self.length == 4:
            self.wordlist = POPULAR_4LETTER_WORDS
        elif self.length == 5:
            self.wordlist = POPULAR_5LETTER_WORDS
        elif self.length == 6:
            self.wordlist = POPULAR_6LETTER_WORDS
        else:
            self.wordlist = []

    def _generate_phonetic(self) -> str:
        """Generates pronounceable natural phonetic syllables of exact length N"""
        start_with_consonant = random.random() < 0.7
        chars = []
        for i in range(self.length):
            is_c = (i % 2 == 0) if start_with_consonant else (i % 2 != 0)
            chars.append(random.choice(CONSONANTS) if is_c else random.choice(VOWELS))
        return "".join(chars)

    def _generate_word_with_digit(self) -> Optional[str]:
        """e.g. 4-letter word + 1 digit for 5 chars, or 1 digit + 4-letter word"""
        if self.length == 5:
            base_word = random.choice(POPULAR_4LETTER_WORDS)
            digit = random.choice(DIGITS)
            return f"{base_word}{digit}" if random.random() < 0.7 else f"{digit}{base_word}"
        elif self.length == 4:
            base_word = random.choice(POPULAR_3LETTER_WORDS)
            digit = random.choice(DIGITS)
            return f"{base_word}{digit}" if random.random() < 0.7 else f"{digit}{base_word}"
        elif self.length == 6:
            base_word = random.choice(POPULAR_5LETTER_WORDS)
            digit = random.choice(DIGITS)
            return f"{base_word}{digit}"
        return None

    def next_username(self) -> Optional[str]:
        for _ in range(50):
            roll = random.random()
            if self.wordlist and roll < 0.55:
                candidate = random.choice(self.wordlist)
            elif roll < 0.85:
                candidate = self._generate_phonetic()
            else:
                digit_cand = self._generate_word_with_digit()
                candidate = digit_cand if digit_cand else self._generate_phonetic()

            if DiscordRuleValidator.is_valid(
                candidate,
                min_len=self.length,
                max_len=self.length,
                check_reserved=self.exclude_reserved
            ):
                return candidate

        return random.choice(self.wordlist) if self.wordlist else self._generate_phonetic()

    def get_pattern_type(self) -> str:
        return f"dictionary_{self.length}char"

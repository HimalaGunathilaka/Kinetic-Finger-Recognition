#pragma once
#include <vector>
#include <SPIFFS.h>
#include <Arduino.h>
#include <algorithm>

// Markov entry structure (packed to 7 bytes: 2 + 1 + 4)
// Python writer packs with struct.pack('3sf', ctx+next, prob) -> 3 chars + 4-byte float
// Without packing, the compiler adds a padding byte before the float (making it 8 bytes) and reading fails.
#pragma pack(push,1)
struct MarkovEntry {
    char context[2];   // 2-character context (no null terminator)
    char nextChar;     // predicted character
    float prob;        // probability (IEEE 754 32-bit)
};
#pragma pack(pop)
static_assert(sizeof(MarkovEntry) == 7, "MarkovEntry must be 7 bytes to match Python binary format");

// Prediction structure
struct Prediction {
    char nextChar;
    float prob;
};

// Database container
extern std::vector<MarkovEntry> markovDB;

// Load Markov binary file from SPIFFS
inline void loadMarkovDB(const char* path = "/markov.bin") {
    if (!SPIFFS.begin(true)) {
        Serial.println("Error mounting SPIFFS");
        return;
    }

    File file = SPIFFS.open(path, "r");
    if (!file) {
        Serial.println("Failed to open markov.bin");
        return;
    }

    markovDB.clear();
    size_t total = file.size();
    Serial.printf("markov.bin size: %u bytes\n", (unsigned)total);

    // Detect record format: either packed 7 bytes (expected) or 8 bytes (with padding after 3 chars)
    bool eightByte = false;
    if (total % 8 == 0 && total % 7 != 0) {
        eightByte = true; // very likely padded format
    } else if (total % 7 == 0 && total % 8 != 0) {
        eightByte = false; // ideal
    } else if (total % 56 == 0) { // heuristic fallback, prefer 8 if ambiguous
        eightByte = true;
    }

    Serial.printf("Detected record format: %s-byte records\n", eightByte ? "8" : "7");

    if (eightByte) {
        const size_t recSize = 8;
        while (file.available() >= (int)recSize) {
            uint8_t buf[8];
            int r = file.read(buf, 8);
            if (r != 8) break;
            MarkovEntry entry;
            entry.context[0] = buf[0];
            entry.context[1] = buf[1];
            entry.nextChar   = buf[2]; // buf[3] is padding
            memcpy(&entry.prob, &buf[4], 4);
            markovDB.push_back(entry);
        }
    } else {
        while (file.available() >= (int)sizeof(MarkovEntry)) {
            MarkovEntry entry;
            int readBytes = file.read((uint8_t*)&entry, sizeof(MarkovEntry));
            if (readBytes != (int)sizeof(MarkovEntry)) {
                Serial.println("[WARN] Partial read encountered, stopping.");
                break;
            }
            markovDB.push_back(entry);
        }
    }
    file.close();
    Serial.print("Loaded "); Serial.print(markovDB.size()); Serial.println(" Markov entries");
    if (!markovDB.empty()) {
        Serial.printf("First entry debug: ctx='%c%c' next='%c' prob=%.5f (struct size=%u)\n",
                      markovDB[0].context[0], markovDB[0].context[1], markovDB[0].nextChar, markovDB[0].prob, (unsigned)sizeof(MarkovEntry));
    }
}

// Get top N predictions given 0,1,2 character context
inline std::vector<Prediction> getTopN(const std::vector<MarkovEntry>& db, const char* context, int len, int N=5) {
    std::vector<Prediction> candidates;

    for (const auto& entry : db) {
        bool match = false;
        if (len == 2) {
            match = (entry.context[0] == context[0] && entry.context[1] == context[1]);
        } else if (len == 1) {
            match = (entry.context[1] == context[0]); // match last char
        } else {
            match = true; // no context
        }

        if (match) {
            candidates.push_back({entry.nextChar, entry.prob});
        }
    }

    // Sort descending by probability
    std::sort(candidates.begin(), candidates.end(), [](const Prediction& a, const Prediction& b) {
        return a.prob > b.prob;
    });

    if (candidates.size() > N) candidates.resize(N);
    return candidates;
}

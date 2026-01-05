# 🎨 Dialogue Settings - Visual Flow Diagrams

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DIALOGUE SETTINGS SYSTEM                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────────────────────┐
                              │                                 │
                    ┌─────────▼─────────┐          ┌───────────▼──────────┐
                    │   UI COMPONENTS   │          │  JAVASCRIPT LOGIC    │
                    └─────────┬─────────┘          └───────────┬──────────┘
                              │                                 │
        ┌─────────────────────┼─────────────────┐              │
        │                     │                 │              │
┌───────▼────────┐  ┌────────▼────────┐  ┌─────▼──────┐      │
│ Settings Button│  │ Settings Modal  │  │ Toggle     │      │
│ (Gear Icon)    │  │                 │  │ Switches   │      │
└────────────────┘  └─────────────────┘  └────────────┘      │
                                                               │
                    ┌──────────────────────────────────────────┤
                    │                                          │
          ┌─────────▼─────────┐                    ┌──────────▼─────────┐
          │ Settings Manager  │                    │  Auto-Record       │
          │ - loadSettings()  │                    │  - triggerAuto...()│
          │ - saveSettings()  │                    └──────────┬─────────┘
          └─────────┬─────────┘                               │
                    │                                          │
          ┌─────────▼─────────┐                    ┌──────────▼─────────┐
          │   localStorage    │                    │  Playback Logic    │
          │ - autoRecord      │                    │ - saveRecording()  │
          │ - autoPlay        │                    │ - systemAudio()    │
          └───────────────────┘                    └────────────────────┘
```

---

## 🔄 User Flow - Manual Mode (Both OFF)

```
┌─────────────────────────────────────────────────────────────┐
│                    MANUAL MODE FLOW                          │
│              (Auto-Record OFF, Auto-Play OFF)                │
└─────────────────────────────────────────────────────────────┘

    START
      │
      ▼
┌──────────────┐
│ Line becomes │
│   active     │
│  (blue box)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ User clicks  │
│  "Enregistrer"│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ User speaks  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ User clicks  │
│  "Arrêter"   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Audio saves  │
│ Player shows │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ User clicks  │
│  Play button │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Audio plays  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Playback ends│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Next line    │
│  highlights  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ User clicks  │
│ next button  │
└──────┬───────┘
       │
       ▼
    REPEAT
```

---

## ⚡ User Flow - Full Auto Mode (Both ON)

```
┌─────────────────────────────────────────────────────────────┐
│                   FULL AUTO MODE FLOW                        │
│              (Auto-Record ON, Auto-Play ON)                  │
└─────────────────────────────────────────────────────────────┘

    START
      │
      ▼
┌──────────────┐
│ Line becomes │
│   active     │
│  (blue box)  │
└──────┬───────┘
       │
       ▼ (AUTOMATIC)
┌──────────────┐
│ Recording    │
│ auto-starts  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ User speaks  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ User clicks  │
│  "Arrêter"   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Audio saves  │
└──────┬───────┘
       │
       ▼ (AUTOMATIC)
┌──────────────┐
│ Audio plays  │
│ immediately  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Playback ends│
└──────┬───────┘
       │
       ▼ (AUTOMATIC)
┌──────────────┐
│ Next line    │
│  highlights  │
└──────┬───────┘
       │
       ▼ (AUTOMATIC)
┌──────────────┐
│ Next line    │
│ auto-starts  │
└──────┬───────┘
       │
       ▼
    REPEAT
```

---

## 🎯 Settings State Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SETTINGS STATES                           │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │  INITIAL STATE   │
                    │  autoRecord: OFF │
                    │  autoPlay: ON    │
                    └────────┬─────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
    ┌───────────────┐  ┌─────────┐  ┌──────────────┐
    │  MANUAL MODE  │  │  SEMI   │  │  FULL AUTO   │
    │  Both OFF     │  │  AUTO   │  │  Both ON     │
    └───────────────┘  └─────────┘  └──────────────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
            ┌──────────────┐  ┌──────────────┐
            │ AutoPlay ON  │  │ AutoRecord ON│
            │ AutoRecord   │  │ AutoPlay OFF │
            │    OFF       │  │              │
            └──────────────┘  └──────────────┘

    User can switch between any state via Settings Modal
```

---

## 💾 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      DATA FLOW                               │
└─────────────────────────────────────────────────────────────┘

    USER ACTION
        │
        ▼
┌───────────────┐
│ Toggle Switch │
│   in Modal    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Click "Save"  │
└───────┬───────┘
        │
        ▼
┌───────────────────────────────────┐
│     saveSettings() Function       │
│  1. Read toggle states            │
│  2. Update settings object        │
│  3. Save to localStorage          │
│  4. Close modal                   │
│  5. Trigger autoRecord if enabled │
└───────┬───────────────────────────┘
        │
        ├─────────────────┬─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ localStorage │  │   settings   │  │ UI Updates   │
│   Storage    │  │    Object    │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │  PERSISTED   │
                  │   SETTINGS   │
                  └──────────────┘
```

---

## 🔄 Auto-Record Trigger Flow

```
┌─────────────────────────────────────────────────────────────┐
│              AUTO-RECORD TRIGGER FLOW                        │
└─────────────────────────────────────────────────────────────┘

    TRIGGER EVENT
    (Line completed OR Page load OR Settings enabled)
        │
        ▼
┌───────────────────┐
│ triggerAutoRecord()│
└────────┬──────────┘
         │
         ▼
    ┌────────────┐
    │ Check if   │───NO──▶ EXIT (Manual mode)
    │ autoRecord │
    │  enabled?  │
    └────┬───────┘
         │ YES
         ▼
    ┌────────────┐
    │ Wait 500ms │
    │ (UI delay) │
    └────┬───────┘
         │
         ▼
    ┌────────────┐
    │ Find active│
    │    line    │
    └────┬───────┘
         │
         ▼
    ┌────────────┐
    │ Line type? │
    └────┬───────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│  User  │ │ System │
│  Line  │ │  Line  │
└───┬────┘ └───┬────┘
    │          │
    ▼          ▼
┌────────┐ ┌────────┐
│ Click  │ │ Click  │
│ Record │ │  Play  │
│ Button │ │ Button │
└────────┘ └────────┘
```

---

## 🎬 Complete Dialogue Flow

```
┌─────────────────────────────────────────────────────────────┐
│           COMPLETE DIALOGUE PROGRESSION                      │
└─────────────────────────────────────────────────────────────┘

START SIMULATION
      │
      ▼
┌──────────────────┐
│ Load Settings    │
│ from localStorage│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Highlight Line 1 │
│   (blue border)  │
└────────┬─────────┘
         │
         ▼
    ┌────────────┐
    │ autoRecord?│
    └────┬───────┘
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ Auto   │ │ Wait   │
│ Start  │ │ User   │
└───┬────┘ └───┬────┘
    │          │
    └────┬─────┘
         │
         ▼
┌──────────────────┐
│ Record/Generate  │
└────────┬─────────┘
         │
         ▼
    ┌────────────┐
    │ autoPlay?  │
    └────┬───────┘
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ Auto   │ │ Wait   │
│ Play   │ │ User   │
└───┬────┘ └───┬────┘
    │          │
    └────┬─────┘
         │
         ▼
┌──────────────────┐
│ Playback Ends    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Update Progress  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Highlight Next   │
│      Line        │
└────────┬─────────┘
         │
         ▼
    ┌────────────┐
    │ More lines?│
    └────┬───────┘
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
  REPEAT   ┌────────┐
           │  END   │
           │DIALOGUE│
           └────────┘
```

---

## 🎨 UI Component Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                  SIMULATION RUN PAGE                         │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌─────────▼────────┐  ┌────────▼────────┐
│  Dialogue Card │  │  Dialogues List  │  │ Progress Card   │
│                │  │      Card        │  │                 │
│  - Line Items  │  │                  │  │ - Header ──────┐│
│  - Record Btn  │  │  - Dialogue 1    │  │   - Title      ││
│  - Play Btn    │  │  - Dialogue 2    │  │   - ⚙️ Button  ││
│  - Audio       │  │  - Dialogue 3    │  │                ││
└────────────────┘  └──────────────────┘  │ - Progress Bar ││
                                           │ - Next Button  ││
                                           └────────────────┘│
                                                    │         │
                                                    ▼         │
                                           ┌─────────────────┐│
                                           │ Settings Modal  ││
                                           │                 ││
                                           │ - Header        ││
                                           │ - Auto-Record   ││
                                           │   Toggle        ││
                                           │ - Auto-Play     ││
                                           │   Toggle        ││
                                           │ - Save Button   ││
                                           └─────────────────┘│
                                                    ▲          │
                                                    └──────────┘
```

---

## 📊 Settings Impact Matrix

```
┌─────────────────────────────────────────────────────────────┐
│              SETTINGS IMPACT ON BEHAVIOR                     │
└─────────────────────────────────────────────────────────────┘

                    AUTO-PLAY
                 OFF  │  ON
              ───────┼───────
         OFF │   1   │   2   │
AUTO-RECORD  ├───────┼───────┤
         ON  │   3   │   4   │
              ───────┴───────

┌─────────────────────────────────────────────────────────────┐
│ MODE 1: Both OFF (Full Manual)                              │
│ ✓ User clicks record                                        │
│ ✓ User clicks stop                                          │
│ ✓ User clicks play                                          │
│ ✓ User clicks next line button                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ MODE 2: Auto-Play ON only (Semi-Auto)                       │
│ ✓ User clicks record                                        │
│ ✓ User clicks stop                                          │
│ ✗ Auto-plays                                                │
│ ✓ User clicks next line button                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ MODE 3: Auto-Record ON only (Custom)                        │
│ ✗ Auto-starts record                                        │
│ ✓ User clicks stop                                          │
│ ✓ User clicks play                                          │
│ ✗ Auto-advances to next line                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ MODE 4: Both ON (Full Auto)                                 │
│ ✗ Auto-starts record                                        │
│ ✓ User clicks stop                                          │
│ ✗ Auto-plays                                                │
│ ✗ Auto-advances to next line                                │
└─────────────────────────────────────────────────────────────┘

Legend: ✓ = User action required  ✗ = Automatic
```

---

*Visual diagrams created to enhance understanding of the Dialogue Settings feature*

# ⚡ Dialogue Settings - Quick Reference Guide

## 🎯 Quick Overview

Two settings control dialogue playback behavior:
1. **Auto-Record**: Auto-trigger recording/TTS when line becomes active
2. **Auto-Play**: Auto-play audio after recording/generation

## 🔑 Key Code Locations

### Settings Object
```javascript
const settings = {
    autoRecord: false,  // Default: OFF
    autoPlay: true      // Default: ON
};
```

### localStorage Keys
- `dialogueAutoRecord` → boolean as string
- `dialogueAutoPlay` → boolean as string

## 📋 Function Reference

### `loadSettings()`
**Purpose**: Load settings from localStorage  
**Called**: On page load  
**Returns**: void  

### `saveSettings()`
**Purpose**: Save settings to localStorage  
**Called**: When user clicks "Enregistrer"  
**Returns**: void  

### `triggerAutoRecord()`
**Purpose**: Auto-trigger recording/playback for active line  
**Called**: After line completion, on page load, when enabling autoRecord  
**Returns**: void  
**Delay**: 500ms for smooth transition  

## 🎬 Behavior Quick Reference

| Setting Combination | What Happens |
|---------------------|--------------|
| Both OFF | Manual record → Manual play → Manual next |
| AutoPlay ON only | Manual record → Auto-play → Manual next |
| AutoRecord ON only | Auto-record → Manual play → Auto-next |
| Both ON | Auto-record → Auto-play → Auto-next (Full automation) |

## 🔧 How to Check Settings

```javascript
// In browser console
console.log(settings);
// Output: {autoRecord: false, autoPlay: true}

// Check localStorage
localStorage.getItem('dialogueAutoRecord'); // "false" or "true"
localStorage.getItem('dialogueAutoPlay');   // "false" or "true"
```

## 🐛 Debugging Tips

### Settings not persisting?
```javascript
// Check if localStorage is available
if (typeof(Storage) !== "undefined") {
    console.log("localStorage is supported");
} else {
    console.log("localStorage NOT supported");
}
```

### Auto-record not triggering?
```javascript
// Check settings state
console.log('Auto-record enabled?', settings.autoRecord);

// Check if active line exists
console.log('Active line:', document.querySelector('.line-active'));
```

### Auto-play not working?
```javascript
// Check settings state
console.log('Auto-play enabled?', settings.autoPlay);

// Check audio element
const audio = document.querySelector('.line-active audio');
console.log('Audio element:', audio);
console.log('Audio src:', audio?.src);
```

## 📝 Adding a New Setting

### Step 1: Add to settings object
```javascript
const settings = {
    autoRecord: false,
    autoPlay: true,
    yourNewSetting: false  // Add here
};
```

### Step 2: Add toggle in modal
```html
<div class="form-check form-switch">
    <input class="form-check-input" type="checkbox" id="yourNewSettingSwitch">
    <label class="form-check-label" for="yourNewSettingSwitch">
        <strong>Your Setting Name</strong>
    </label>
</div>
```

### Step 3: Update loadSettings()
```javascript
const savedYourSetting = localStorage.getItem('dialogueYourNewSetting');
if (savedYourSetting !== null) {
    settings.yourNewSetting = savedYourSetting === 'true';
}
document.getElementById('yourNewSettingSwitch').checked = settings.yourNewSetting;
```

### Step 4: Update saveSettings()
```javascript
settings.yourNewSetting = document.getElementById('yourNewSettingSwitch').checked;
localStorage.setItem('dialogueYourNewSetting', settings.yourNewSetting);
```

### Step 5: Apply logic
```javascript
if (settings.yourNewSetting) {
    // Your custom behavior
}
```

## 🎯 Common Use Cases

### Reset Settings to Default
```javascript
localStorage.removeItem('dialogueAutoRecord');
localStorage.removeItem('dialogueAutoPlay');
location.reload(); // Reload page to apply defaults
```

### Force Enable Auto-Record
```javascript
settings.autoRecord = true;
localStorage.setItem('dialogueAutoRecord', 'true');
document.getElementById('autoRecordSwitch').checked = true;
triggerAutoRecord(); // Start immediately
```

### Disable All Automation
```javascript
settings.autoRecord = false;
settings.autoPlay = false;
localStorage.setItem('dialogueAutoRecord', 'false');
localStorage.setItem('dialogueAutoPlay', 'false');
```

## 🔍 Testing Checklist

- [ ] Settings save when clicking "Enregistrer"
- [ ] Settings load on page refresh
- [ ] Auto-record triggers for user lines
- [ ] Auto-record triggers for system lines
- [ ] Auto-play works for recordings
- [ ] Auto-play works for TTS
- [ ] Manual mode works (both OFF)
- [ ] Full automation works (both ON)
- [ ] Modal opens/closes properly
- [ ] Toggle switches reflect saved state

## 📞 Support

**File Location**: `simulator/templates/simulator/simulation_run.html`  
**Lines**: ~180-400 (settings section)  
**Dependencies**: Bootstrap 5, localStorage API  

**Common Issues**:
1. Modal not opening → Check Bootstrap JS is loaded
2. Settings not saving → Check localStorage permissions
3. Auto-record not working → Check microphone permissions

---

**Last Updated**: 2024  
**Version**: 1.0

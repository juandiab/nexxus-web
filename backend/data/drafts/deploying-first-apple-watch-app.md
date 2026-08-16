# Deploying My First Apple Watch App

Most of my production deploys involve load balancers, WAF profiles, and change windows. Shipping a watchOS app is a different kind of first release: a 44mm screen, a signing chain that still thinks in iOS containers, and a store listing that will reject you for a missing usage string. This is the path I wish I had printed before I hit Archive the first time.

This is a first-ship guide, not a SwiftUI tutorial. If the app already runs in the simulator, the remaining work is project shape, signing, TestFlight, and App Store Connect metadata.

## Pick the project shape before you write more code

Apple supports three shapes. Pick one on day one. Changing later is possible, but it rewrites bundle IDs, entitlements, and the App Store record.

| Shape | When to use it | What the user installs |
|-------|----------------|------------------------|
| **Watch-only** | The iPhone app would be an empty shell | Apple Watch only |
| **Independent watch + iPhone** | Phone and watch are useful on their own | Either, or both |
| **Dependent watch + iPhone** | The watch app cannot work without the phone | Watch waits until the iPhone app is installed |

For a first app, **Watch-only** is the cleanest path if you do not need HealthKit sync, WatchConnectivity, or a phone UI. Apple documents this as an [independent watchOS app](https://developer.apple.com/documentation/watchos-apps/creating-independent-watchos-apps/). Users expect the watch app to work when the iPhone is in another room. Independent is the default you want unless you have a hard dependency.

If you already started from an iOS app and added a Watch App target, you can still mark the watch app independent: enable **Supports Running Without iOS App Installation** on the watch target. That is the conversion Apple describes when a companion exists but the watch should stand alone.

## What you need before Xcode will let you ship

- A paid **Apple Developer Program** membership. Simulator builds do not require it. Device installs, TestFlight, and the App Store do.
- **Xcode** current enough for the watchOS SDK you are targeting. Pair the watchOS deployment target with a watch you actually own.
- An **iPhone** paired with the Apple Watch you will test on. The watch debugger rides through the phone.
- A **bundle ID** you will not rename later. The App Store record is tied to it.

Create the App ID in the developer portal only if you need explicit capabilities (HealthKit, Push, App Groups). For a first app with Automatic Signing, Xcode can register the IDs when you first run on a device.

## Create the Watch-only project

In Xcode:

1. **File → New → Project**
2. Open the **watchOS** tab
3. Choose **App**
4. Select **Watch-only App**
5. Enable tests if you want them; skip Core Data unless you already know you need it

That template is doing more than it looks. It creates the watch app target **and** a tiny iOS container that App Store Connect expects. The container is not a product you open on iPhone. It is the delivery vehicle. If you skip it and archive a bare watchOS target, Organizer often shows only Ad Hoc, Enterprise, and Debugging — no App Store Connect tile. That is not a signing bug. Xcode has no watchOS App Store distribution method of its own.

Keep the bundle IDs nested:

- iOS container: `com.yourname.firstwatch`
- Watch app: `com.yourname.firstwatch.watchkitapp`

Version and build number must match across both targets. App Store Connect rejects the upload when they drift.

On the watch app Info settings:

- `WKWatchOnly` = `YES`
- Do **not** set `WKCompanionAppBundleIdentifier` for a true watch-only app

The container can carry two flags that tell the store this is not an iPhone product:

- `ITSWatchOnlyContainer` = `YES`
- `LSApplicationLaunchProhibited` = `YES`

The official Watch-only template sets this up. If you assembled the project by hand, missing those keys is why the listing suddenly demands iPhone screenshots.

## Run it on a simulator, then on a real watch

The simulator is enough to prove navigation, layout, and Digital Crown behavior. It is not enough to prove HealthKit permissions, haptics, always-on display, or WatchConnectivity.

For a device run:

1. Unlock the iPhone and the watch. Trust the Mac if prompted.
2. In Xcode, select the watch app scheme and your paired watch.
3. Enable **Automatic Signing** on every target, using the same team.
4. Run. The first install is slow. The watch shows a spinner, not a crash.

If the run destination is missing, the watch is not paired, not unlocked, or still finishing a watchOS update. Xcode will not argue. It just omits the device.

## Capabilities and privacy strings

Anything that touches user data needs a usage description **before** you archive. The simulator may let you skip this. App Store validation will not.

Common first-app ones:

| Capability | Info.plist key | Write it in plain language |
|------------|----------------|----------------------------|
| HealthKit | `NSHealthShareUsageDescription` / `NSHealthUpdateUsageDescription` | Why you read or write health data |
| Location | `NSLocationWhenInUseUsageDescription` | Why the watch needs location |
| Motion | `NSMotionUsageDescription` | Why you read the accelerometer |
| Notifications | permission request in code | Ask only when the user can see why |

Add the capability on the watch target, not only on the container. Then add the usage string on the target that actually requests the permission.

Also decide **export compliance** early. If the app only uses HTTPS through Apple system libraries, you can set `ITSAppUsesNonExemptEncryption` to `NO` in the container Info.plist and skip the annual encryption questionnaire on every upload. If you ship your own crypto, do not set that flag.

## Archive like an iOS app

This is the step that feels wrong the first time.

1. Select **Any watchOS Device (arm64_32)** — not a simulator.
2. Confirm the scheme's **Archive** action builds the iOS container, which embeds the watch app.
3. **Product → Archive**
4. In Organizer the archive should appear as an **iOS** archive. That is expected.
5. **Validate App**, then **Distribute App → App Store Connect**

If Organizer only offers Ad Hoc, the scheme archived the watch target instead of the container. Fix the Archive action, or recreate the project from the Watch-only template and move your Swift files over. Fighting a bare watchOS archive wastes a night.

After a successful upload, the build appears under an **iOS** app record in App Store Connect. There is no separate watchOS platform picker. Apple's own help says you [create an iOS app and then add watchOS information](https://developer.apple.com/help/app-store-connect/create-an-app-record/add-watchos-app-information).

## Create the App Store Connect record

1. App Store Connect → **My Apps → + → New App**
2. Platform: **iOS**
3. Bundle ID: the **container** ID (`com.yourname.firstwatch`)
4. Open the version and fill the **Apple Watch** tab under Previews and Screenshots

For a watch-only app you need Watch screenshots and an app icon. You do **not** need iPhone screenshots. If the form insists on iPhone media, the store still thinks you shipped a companion. Check `ITSWatchOnlyContainer` and that the uploaded binary is classified as watch-only.

Write the description so a reviewer can tell what the app does **on the watch**. Mention complications, always-on, or offline behavior if you have them. App Review looks at the Watch screenshots, not your iPhone marketing copy.

Privacy Nutrition Labels are required before submit. Be honest. A first app that only stores settings on-device is usually **Data Not Collected**. HealthKit changes that immediately.

## TestFlight before the store

Upload the same archive you intend to ship. TestFlight is not a different binary type.

- **Internal testers** (up to 100 people on your App Store Connect team) can install as soon as processing finishes. Use this for the first watch install.
- **External testers** can require Beta App Review on the first build.

Testers install **TestFlight on iPhone**, accept the invite, then install the watch app onto Apple Watch from the TestFlight or Watch app flow. A watch-only product still starts on the phone because that is how Apple delivers the container.

A build stays testable for **90 days**. Bump the build number for every upload. Keep the marketing version stable until you actually ship 1.0.

Walk the watch with the phone in another room. That is the test the simulator cannot fake: independent install, permissions, and any network call you assumed would ride the phone.

## The mistakes that blocked my first upload

These are the failures I hit or watched other first-time watch submissions hit. None of them are Swift bugs.

- **Version or build mismatch** between the container and the watch app. Set both in one place and copy them.
- **Archived the watch target.** Organizer looks fine until the App Store Connect tile is missing.
- **Usage strings on the wrong target.** HealthKit on the watch, description only on iOS — validation fails.
- **Automatic Signing on one target, manual on the other.** Pick one model. Automatic is enough for a first app.
- **Simulator destination in Archive.** The archive must be a device build (`arm64_32` for watchOS).
- **Missing encryption declaration.** Set `ITSAppUsesNonExemptEncryption` or answer the questionnaire every time.
- **Watch screenshots at the wrong size.** Use the [screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications) for the watch sizes you support.
- **Dependent app pretending to be independent.** If the watch cannot launch without the iPhone app, do not advertise watch-only.

## First-ship checklist

- [ ] Watch-only or independent watch app, not an accidental dependent companion
- [ ] Nested bundle IDs; matching version and build on every target
- [ ] Automatic Signing, same team, device install works on a real watch
- [ ] Usage descriptions for every permission you request
- [ ] `ITSAppUsesNonExemptEncryption` decided
- [ ] Archive is an iOS container that embeds the watch app
- [ ] App Store Connect record uses the container bundle ID
- [ ] Apple Watch screenshots and icon uploaded
- [ ] Internal TestFlight install on a physical watch
- [ ] Privacy labels completed before Submit for Review

## What I would do again

I would still start from the **Watch-only App** template, even if I later add an iPhone companion. The container, the store record, and the archive flow are the parts that are easy to get wrong and slow to unwind.

I would also treat TestFlight on a real watch as the first production environment. The simulator proved the UI. The watch on my wrist proved permissions, install, and the independent-app promise.

The code was the easy part. The release was a packaging problem: give App Store Connect an iOS-shaped box that only contains a watch.

Official starting points: [Creating independent watchOS apps](https://developer.apple.com/documentation/watchos-apps/creating-independent-watchos-apps/), [Distributing your app](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases), and [watchOS app information in App Store Connect](https://developer.apple.com/help/app-store-connect/create-an-app-record/add-watchos-app-information).

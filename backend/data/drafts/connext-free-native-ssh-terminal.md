# ConneXt: A Free Native SSH Terminal for iPhone and iPad

Most of the SSH clients I have used on a phone feel like a compromise: a web view in a native shell, a paywall in front of split sessions, or a subscription for keys I already own. I wanted the opposite. **ConneXt** is a native SSH terminal for iPhone and iPad that I built at Nexxus-Tech — Liquid Glass navigation, split terminals, reusable imported keys, and an optional Command Assistant. It is **free**. There is no subscription and no in-app purchase.

This is a product note, not a tutorial. If you already live in a shell, here is what ConneXt is, what it is not, and where the data goes.

## What it is

ConneXt is a **native iOS / iPadOS** SSH client. It is not a remote-desktop wrapper and not a chat app dressed as a terminal. You add the hosts you already operate, import the keys you already use, and work in sessions that belong on a phone or an iPad.

I built it because that is how I work: jump on a load balancer from a hotel Wi-Fi, read `nsconmsg` on an iPad next to a change window, keep a second pane open without paying a monthly tax for the privilege.

| Fact | Detail |
|------|--------|
| **Price** | Free. No subscription. No IAP. |
| **Platform** | iPhone and iPad — iOS / iPadOS |
| **Accounts** | None. ConneXt does not create user accounts. |
| **Author** | Juan Pablo Otalvaro · Nexxus-Tech |

Product page: [nexxus-tech.com/connext](/connext). Support: [nexxus-tech.com/connext/support](/connext/support). Privacy: [nexxus-tech.com/connext/privacy](/connext/privacy).

## Who it is for

Network engineers, SREs, and anyone who needs a serious SSH client when the laptop is closed.

- Operators who jump on a host from a phone or iPad
- Engineers who import keys once and reuse them across hosts
- Anyone who wants a native client without a paywall

If you need a team SaaS, a shared session recorder, or a hosted jump box, this is not that product. ConneXt talks to **the servers you configure**. Nothing is brokered through Nexxus-Tech.

## What it does

The surface is small on purpose.

**Liquid Glass navigation.** The shell follows Apple’s Liquid Glass language so the terminal stays the focus. This is a native app, not a web view.

**Split terminals.** Open more than one session on screen. That is the iPad use case I actually have — and the phone use case when two hosts have to be in view at once.

**Reusable imported keys.** Import a key once. Reuse it across hosts. Private keys stay in the **iOS Keychain** on the device.

**Optional Command Assistant.** When you want help drafting a command, you can enable an assistant and bring your own **OpenAI**, **Gemini**, or **Anthropic** key. It is off unless you turn it on. The assistant is included — it is not an upgrade SKU. You pay the provider you choose for inference, if you use it at all.

## What stays on the device

I will not ask you to trust a ConneXt account, because there isn’t one.

- SSH passwords and private keys are stored in the **iOS Keychain** on your device.
- Connections go only to hosts **you** add.
- Optional AI API keys stay on the device. Prompts go only to the provider **you** enable — OpenAI, Gemini, or Anthropic.
- ConneXt does not sell personal data.

That is the whole privacy model. The policy is on the site: [ConneXt Privacy Policy](/connext/privacy).

## What it does not do

- It does not create a Nexxus-Tech login.
- It does not proxy your SSH through our cloud.
- It does not require a subscription to unlock split sessions, keys, or the assistant.
- It does not ship your private keys to an LLM. Credentials stay in Keychain.

If a vendor’s SSH app is a funnel into a paid tier, ConneXt is the other direction.

## Requirements

A compatible **iPhone or iPad** running **iOS / iPadOS**. You need a host that accepts SSH and, if you use public-key auth, a key you can import.

The Command Assistant is optional. If you never add an AI key, ConneXt is still a full SSH client.

## Where to get it

The App Store listing is in progress. Until it is live, the marketing, support, and privacy URLs App Store Connect needs are already up:

- Marketing: [https://nexxus-tech.com/connext](https://nexxus-tech.com/connext)
- Support: [https://nexxus-tech.com/connext/support](https://nexxus-tech.com/connext/support)
- Privacy: [https://nexxus-tech.com/connext/privacy](https://nexxus-tech.com/connext/privacy)

The store CTA currently points at a placeholder (`https://apps.apple.com/app/connext`) until Apple assigns the real listing.

Questions: [support@nexxus-tech.com](mailto:support@nexxus-tech.com).

## Why I shipped it this way

I spend most days on NetScaler, WAF, and change control. The phone is not a toy in that work — it is the device I have when I need a shell. ConneXt is the client I wanted for that moment: native, readable, keyed from the Keychain, and free enough that I will not hesitate to install it on a spare iPad.

© Nexxus-Tech / Juan Pablo Otalvaro.

*[Product page](/connext) · [Support](/connext/support) · [Contact Nexxus Tech](/contact) if you want to talk about how we work — consulting, JPilot, or the rest of the stack.*

# Omni Reference – Midjourney
Source: https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference
Omni Reference – Midjourney














Midjourney Docs

[Skip to main content](#page-container)

[![Midjourney Help Center home page](/hc/theming_assets/01K1K3SHJHG4BTD9YK9VH9G86N)

Midjourney](/hc/en-us)


Toggle navigation menu





1. [Midjourney](/hc/en-us)
2. [Documentation](/hc/en-us/categories/32013335627533-Documentation)
3. [Using Your Own Images](/hc/en-us/sections/32013397184397-Using-Your-Own-Images)

# Omni Reference

### Want to put a person or object into your images? You can provide Midjourney with an Omni Reference!

[![omni-ref-header.png](/hc/article_attachments/36285152349837)](https://docs.midjourney.com/hc/article_attachments/36285152349837)

Adding an Omni Reference image to the Imagine bar will automatically run the prompt in V7. For more information about V8.1, see our [Version](/hc/en-us/articles/32199405667853) article.

## What is an Omni Reference?

Using an Omni Reference allows you to put characters, objects, vehicles, or non-human creatures from a reference image into your Midjourney creations.

You can use it in combination with [Personalization](/hc/en-us/articles/32433330574221), [Moodboards](/hc/en-us/articles/39193335040013), [stylize](/hc/en-us/articles/32196176868109), and [Style References!](/hc/en-us/articles/32180011136653)

Omni Reference is compatible with Midjourney version 7.

• Omni Reference is not compatible with features like inpainting or outpainting that still use V6.1.  
• Using Omni Reference will cost 2x more [GPU time](/hc/en-us/articles/32016412137741) compared to regular V7 images.  
• Omni Reference image results currently are not compatible with [Vary Region](/hc/en-us/articles/32794723105549), [Pan](/hc/en-us/articles/32570788043405), or [Zoom Out](/hc/en-us/articles/32595476770957). To edit these images please load them into the [Editor](/hc/en-us/articles/32764383466893) on midjourney.com and remove the image reference and any `--oref` or `--ow` parameters.  
• Omni Reference is currently not compatible with [Fast Mode](/hc/en-us/articles/32016412137741), [Draft Mode & Conversational Mode](/hc/en-us/articles/35577175650957), or `--q 4`.

## Using an Omni Reference

* [On Web](#zp-1-0)
* [In Discord](#zp-1-1)

To add an image to your prompt, start by clicking on the image [![image-icon.svg](/hc/article_attachments/36285130548237)](https://docs.midjourney.com/hc/article_attachments/36285130548237) icon in the Imagine bar. This opens the images panel, allowing you to upload new images or pick from those you've already uploaded.

[![omni-ref-ui.png](/hc/article_attachments/36285130549389)](https://docs.midjourney.com/hc/article_attachments/36285130549389)

Drag and drop your image from the uploads library into the Omni Reference section. You can only use one image with Omni Reference. To remove your image from the Imagine bar, hover your mouse over it and click the X icon.

If you want to use your images with multiple prompts, click the lock icon [![lock-icon.svg](/hc/article_attachments/36285130551437)](https://docs.midjourney.com/hc/article_attachments/36285130551437) to keep your images pinned to the Imagine bar.

**Image Reference Types:**  
[![video-frame-icon.svg](/hc/article_attachments/38169342150285)](https://docs.midjourney.com/hc/article_attachments/38169342150285) [Starting Frame](/hc/en-us/articles/37460773864589)  
[![image-prompt-icon.svg](/hc/article_attachments/36285152370317)](https://docs.midjourney.com/hc/article_attachments/36285152370317) [Image Prompt](/hc/en-us/articles/32040250122381)   
[![style-reference-icon.svg](/hc/article_attachments/36285130552973)](https://docs.midjourney.com/hc/article_attachments/36285130552973) [Style Reference](/hc/en-us/articles/32180011136653)  
[![character-reference-icon.svg](/hc/article_attachments/36285130553229)](https://docs.midjourney.com/hc/article_attachments/36285130553229) Omni Reference (V7)

To use an Omni Reference in Discord, start by adding the `--oref` parameter to the end of your prompt, then pasting your image URL. You can only use one image with Omni Reference.

[![discord-oref.png](/hc/article_attachments/36285152373389)](https://docs.midjourney.com/hc/article_attachments/36285152373389)

It's important to ensure that you have a valid image URL, meaning the image should already be online. If your image is stored on your computer or device, you can [host it on Discord](/hc/en-us/articles/32558957919117) to generate an image URL.

## Best Practices

* **Importance of Text Prompts:** Combine your Omni Reference with a clear text prompt. Text is just as important for conveying the full scene and additional details beyond what the reference image shows.
* **Reinforce the Style:** If you want your image in a different style than your reference, mention your desired style at both the start and end of your prompt. For example, "**Illustration** of a young woman with short gray hair **drawn by a comic book artist**." Also consider using [style references](/hc/en-us/articles/32180011136653) and lowering the [Omni Reference weight](#h_01JD5G8C3RY38GSHNSFH6H7H31). With a lower weight you will need to reinforce the physical characteristics you want to preserve using your prompt text.
* **Multiple Characters:** While you can only use one image as an Omni Reference, you can try using an image that contains multiple characters/people and describe them in your prompt.
* **Account for Details:** Be aware that intricate details like specific freckles or logos on clothing may not perfectly match your reference.
* **Consider Other Parameters:** If you're using high [stylize](/hc/en-us/articles/32196176868109) or `--exp` values you may want to also use a higher [Omni Reference Weight](#h_01JD5G8C3RY38GSHNSFH6H7H31), as these will all compete for influence.

* [## External Image Rules & Requirements](#zp-2-0)

  Midjourney provides you with powerful tools for unleashing your imagination. When using our tools to create with external images, we have additional necessary precautions you should be aware of.

  By using external images with Midjourney, you agree to the following rules in addition to our [Terms of Service](/hc/en-us/articles/32083055291277).

  #### External Image Guidelines

  + You must meet the age requirement in our [Terms of Service](/hc/en-us/articles/32083055291277).
  + You must follow all applicable laws, our [Community Guidelines](/hc/en-us/articles/32013696484109), and other policies.
  + We may remove content or restrict access at our discretion.

  #### Your Responsibilities

  + You are responsible for all content you input, create, and share.
  + You must have the necessary rights to use the images you upload.
  + Do not manipulate images of public or private individuals in ways that are abusive, disrespectful, offensive, derogatory, or inflammatory—this includes sexualized deepfakes.
  + Anyone attempting to violate our [Community Guidelines](/hc/en-us/articles/32013696484109) will face suspension or banning without refund. Use these tools with respect and consideration for others.

  **If you disagree with these rules, do not use Midjourney with external images.**

  You will likely encounter friction with our moderation — seemingly innocent prompts may be blocked by our filters. Blocked jobs don't cost you any credits. [GPU time](/hc/en-us/articles/32016412137741) will only be deducted when you see your results.

  We encourage you to use this tool and your imagination with joy, wonder, responsibility, and respect.

  For additional information on policies, including privacy, payments, and disputes, refer to our [Terms of Service](/hc/en-us/articles/32083055291277).

## Omni Reference Weight

The omni reference weight parameter `--ow` allows you to control how much detail from your reference image appears in your new image. You can set this parameter to any value between 1 and 1,000, with the default being `--ow 100`.

Unless you are using a very high [stylize](/hc/en-us/articles/32196176868109) value, it's best to keep your weight below 400, otherwise your results may be unpredictable.

On midjourney.com you can use the Omni Strength slider in the Imagine bar to adjust the weight.

[![omni-ref-weights.png](/hc/article_attachments/36285152374029)](https://docs.midjourney.com/hc/article_attachments/36285152374029)

* [## More Information](#zp-3-0)

  • For your prompts to work, you need a text prompt in combination with your Omni Reference.  
  • Your image file should end in .png, .gif, .webp, .jpg, or .jpeg.  
  • Omni Reference can only be used with Midjourney version 7.  
  • Omni Reference can be combined with [Style References](/hc/en-us/articles/32180011136653) and [Image Prompts](/hc/en-us/articles/32040250122381).

Need Help Getting Started?  
  
[Getting Started Guide](/hc/en-us/articles/33329261836941)

### In this article

1. [What is an Omni Reference?](#h_01JCRMNN0AZ8FBPV109XGJETN6)
2. [Using an Omni Reference](#h_01JCRMPT77EVWXDF6X1DG95BK0)
3. [Best Practices](#h_01JDJ3Y9ZW5R0NWJQ5517NA37E)
4. [External Image Rules & Requirements](#heading-4)
5. [Omni Reference Weight](#h_01JD5G8C3RY38GSHNSFH6H7H31)
6. [More Information](#heading-6)

### Categories

* [Documentation](https://docs.midjourney.com/hc/en-us/categories/32013335627533-Documentation)

  + Getting Started

    - [Getting Started Guide](https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide)
  + Prompting Basics

    - [Prompt Basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics)
    - [Modifying Your Creations](https://docs.midjourney.com/hc/en-us/articles/33329329805581-Modifying-Your-Creations)
    - [Aspect Ratio](https://docs.midjourney.com/hc/en-us/articles/31894244298125-Aspect-Ratio)
    - [Image Size & Resolution](https://docs.midjourney.com/hc/en-us/articles/33329374594957-Image-Size-Resolution)
    - [Art of Prompting](https://docs.midjourney.com/hc/en-us/articles/32835253061645-Art-of-Prompting)
  + Using Your Own Images

    - [Video](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video)
    - [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts)
    - [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
    - [Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
    - [Character Reference](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)
    - [Describe](https://docs.midjourney.com/hc/en-us/articles/32497889043981-Describe)
    - [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor)
  + Using the Website

    - [Website Overview](https://docs.midjourney.com/hc/en-us/articles/33329460426765-Website-Overview)
    - [Creating on Web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web)
    - [Organizing Your Creations](https://docs.midjourney.com/hc/en-us/articles/33329462451469-Organizing-Your-Creations)
    - [Using Folders](https://docs.midjourney.com/hc/en-us/articles/34580542725645-Using-Folders)
    - [Draft & Conversational Modes](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes)
    - [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization)
    - [Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards)
    - [Style Creator](https://docs.midjourney.com/hc/en-us/articles/41308374558221-Style-Creator)
    - [Profiles](https://docs.midjourney.com/hc/en-us/articles/41117938447629-Profiles)
    - [Complete Tasks](https://docs.midjourney.com/hc/en-us/articles/33390759197197-Complete-Tasks)
    - [Transitioning to Web](https://docs.midjourney.com/hc/en-us/articles/41268334793613-Transitioning-to-Web)
  + Midjourney Controls

    - [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
    - [Chaos / Variety](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety)
    - [Legacy Features](https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features)
    - [Multi-Prompts & Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights)
    - [No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No)
    - [Pan](https://docs.midjourney.com/hc/en-us/articles/32570788043405-Pan)
    - [Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations)
    - [Quality](https://docs.midjourney.com/hc/en-us/articles/32176522101773-Quality)
    - [Raw](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw)
    - [Remix](https://docs.midjourney.com/hc/en-us/articles/32799074515213-Remix)
    - [Repeat](https://docs.midjourney.com/hc/en-us/articles/32757107922061-Repeat)
    - [Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds)
    - [Stylize](https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize)
    - [Text Generation](https://docs.midjourney.com/hc/en-us/articles/32502277092109-Text-Generation)
    - [Tile](https://docs.midjourney.com/hc/en-us/articles/32197978340109-Tile)
    - [Upscalers](https://docs.midjourney.com/hc/en-us/articles/32804058614669-Upscalers)
    - [Variations](https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations)
    - [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)
    - [Weird](https://docs.midjourney.com/hc/en-us/articles/32390120435085-Weird)
    - [Zoom Out](https://docs.midjourney.com/hc/en-us/articles/32595476770957-Zoom-Out)
  + Using Discord

    - [Web vs Discord](https://docs.midjourney.com/hc/en-us/articles/33329300781837-Web-vs-Discord)
    - [Discord Quick Start](https://docs.midjourney.com/hc/en-us/articles/32631709682573-Discord-Quick-Start)
    - [Discord Overview](https://docs.midjourney.com/hc/en-us/articles/33330535666445-Discord-Overview)
    - [Discord Direct Messages](https://docs.midjourney.com/hc/en-us/articles/32637339216013-Discord-Direct-Messages)
    - [Add Midjourney to Your Discord Server](https://docs.midjourney.com/hc/en-us/articles/32637946450445-Add-Midjourney-to-Your-Discord-Server)
    - [Discord Command List](https://docs.midjourney.com/hc/en-us/articles/32894521590669-Discord-Command-List)
    - [Creation Settings in Discord](https://docs.midjourney.com/hc/en-us/articles/32868982949517-Creation-Settings-in-Discord)
    - [Info Command](https://docs.midjourney.com/hc/en-us/articles/32084927086861-Info-Command)
    - [Show Command](https://docs.midjourney.com/hc/en-us/articles/32635695384461-Show-Command)
    - [Vary Region](https://docs.midjourney.com/hc/en-us/articles/32794723105549-Vary-Region)
    - [Blend Images in Discord](https://docs.midjourney.com/hc/en-us/articles/32635189884557-Blend-Images-in-Discord)
    - [Hosting Images in Discord](https://docs.midjourney.com/hc/en-us/articles/32558957919117-Hosting-Images-in-Discord)
  + Midjourney Policies

    - [Terms of Service](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service)
    - [Community Guidelines](https://docs.midjourney.com/hc/en-us/articles/32013696484109-Community-Guidelines)
    - [Privacy Policy](https://docs.midjourney.com/hc/en-us/articles/32083472637453-Privacy-Policy)
    - [Cookie Policy](https://docs.midjourney.com/hc/en-us/articles/37012090959245-Cookie-Policy)
    - [Midjourney Trademark Policy](https://docs.midjourney.com/hc/en-us/articles/32084281102349-Midjourney-Trademark-Policy)
    - [Data Deletion and Privacy FAQ](https://docs.midjourney.com/hc/en-us/articles/32084462534541-Data-Deletion-and-Privacy-FAQ)
    - [Purchase Order Terms and Conditions](https://docs.midjourney.com/hc/en-us/articles/32084601469581-Purchase-Order-Terms-and-Conditions)
    - [AB2013 Documentation](https://docs.midjourney.com/hc/en-us/articles/42829949256205-AB2013-Documentation)
* [Billing Support](https://docs.midjourney.com/hc/en-us/categories/16016577793421-Billing-Support)

  + Plan Information

    - [How to Subscribe](https://docs.midjourney.com/hc/en-us/articles/31974654274573-How-to-Subscribe)
    - [Comparing Midjourney Plans](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans)
    - [GPU Speed (Fast, Relax, Turbo)](https://docs.midjourney.com/hc/en-us/articles/32016412137741-GPU-Speed-Fast-Relax-Turbo)
    - [Subscription Fast Time Expiration](https://docs.midjourney.com/hc/en-us/articles/27870521824653-Subscription-Fast-Time-Expiration)
    - [Purchasing Extra Fast Time](https://docs.midjourney.com/hc/en-us/articles/33570952624141-Purchasing-Extra-Fast-Time)
    - [Earning Free Fast Time](https://docs.midjourney.com/hc/en-us/articles/28014817524109-Earning-Free-Fast-Time)
    - [Using Images & Videos Commercially](https://docs.midjourney.com/hc/en-us/articles/27870375276557-Using-Images-Videos-Commercially)
    - [Stealth Mode](https://docs.midjourney.com/hc/en-us/articles/32019750070669-Stealth-Mode)
    - [Keeping Your Creations Private](https://docs.midjourney.com/hc/en-us/articles/28014645615373-Keeping-Your-Creations-Private)
    - [Free Trials](https://docs.midjourney.com/hc/en-us/articles/27870399340173-Free-Trials)
    - [Discord Nitro Subscription](https://docs.midjourney.com/hc/en-us/articles/27870371412749-Discord-Nitro-Subscription)
  + Account Management

    - [Logging In & Connecting Accounts](https://docs.midjourney.com/hc/en-us/articles/33390994570509-Logging-In-Connecting-Accounts)
    - [Managing Your Subscription](https://docs.midjourney.com/hc/en-us/articles/28014179406861-Managing-Your-Subscription)
    - [Finding Your Renewal Time](https://docs.midjourney.com/hc/en-us/articles/27870433501837-Finding-Your-Renewal-Time)
    - [Upgrading or Downgrading Your Plan](https://docs.midjourney.com/hc/en-us/articles/27870428114317-Upgrading-or-Downgrading-Your-Plan)
    - [Using Midjourney in Discord](https://docs.midjourney.com/hc/en-us/articles/31541509949069-Using-Midjourney-in-Discord)
    - [Turning Off Automatic Renewals](https://docs.midjourney.com/hc/en-us/articles/27868888211213-Turning-Off-Automatic-Renewals)
    - [Changing Your Billing Email](https://docs.midjourney.com/hc/en-us/articles/27868854770573-Changing-Your-Billing-Email)
    - [Transferring Your Subscription](https://docs.midjourney.com/hc/en-us/articles/31541557571981-Transferring-Your-Subscription)
    - [Deleting Your Data](https://docs.midjourney.com/hc/en-us/articles/27870397554701-Deleting-Your-Data)
    - [Contacting Support](https://docs.midjourney.com/hc/en-us/articles/32638309968141-Contacting-Support)
  + Payments

    - [Accepted Payment Methods](https://docs.midjourney.com/hc/en-us/articles/27868831972365-Accepted-Payment-Methods)
    - [Editing Your Payment Information](https://docs.midjourney.com/hc/en-us/articles/25385791792781-Editing-Your-Payment-Information)
    - [Viewing Your Payment History](https://docs.midjourney.com/hc/en-us/articles/27868885185293-Viewing-Your-Payment-History)
    - [Unsuccessful Payments](https://docs.midjourney.com/hc/en-us/articles/27868801964045-Unsuccessful-Payments)
    - [Fixing a Paused Plan](https://docs.midjourney.com/hc/en-us/articles/27868802467853-Fixing-a-Paused-Plan)
    - [Payment Currency](https://docs.midjourney.com/hc/en-us/articles/27868831424525-Payment-Currency)
    - [Reporting a Duplicate Charge](https://docs.midjourney.com/hc/en-us/articles/27868806085517-Reporting-a-Duplicate-Charge)
    - [Reporting an Unauthorized Charge](https://docs.midjourney.com/hc/en-us/articles/27868804543885-Reporting-an-Unauthorized-Charge)
    - [Changing Your Invoice Information](https://docs.midjourney.com/hc/en-us/articles/27868825749517-Changing-Your-Invoice-Information)
    - [Group Plans & Corporate Billing](https://docs.midjourney.com/hc/en-us/articles/27870607078285-Group-Plans-Corporate-Billing)
    - [Educational Use & Student Billing](https://docs.midjourney.com/hc/en-us/articles/42428820154765-Educational-Use-Student-Billing)
  + Cancellations & Refunds

    - [Canceling Your Subscription](https://docs.midjourney.com/hc/en-us/articles/25384024738573-Canceling-Your-Subscription)
    - [Requesting a Refund](https://docs.midjourney.com/hc/en-us/articles/25386088618253-Requesting-a-Refund)
  + Taxes & VAT

    - [Tax / VAT Charges](https://docs.midjourney.com/hc/en-us/articles/27868801261325-Tax-VAT-Charges)
    - [Setting Your Organization's Tax Status (VAT & Tax Exemptions)](https://docs.midjourney.com/hc/en-us/articles/27868838932621-Setting-Your-Organization-s-Tax-Status-VAT-Tax-Exemptions)
  + Magazines & Books

    - [Midjourney Magazine Subscription FAQ](https://docs.midjourney.com/hc/en-us/articles/28012940139021-Midjourney-Magazine-Subscription-FAQ)
    - [Managing Your Midjourney Magazine Subscription](https://docs.midjourney.com/hc/en-us/articles/27870410169997-Managing-Your-Midjourney-Magazine-Subscription)
    - [Midjourney Store Orders FAQ](https://docs.midjourney.com/hc/en-us/articles/28012925933837-Midjourney-Store-Orders-FAQ)



[Midjourney Website](https://www.midjourney.com)
[Midjourney Discord Server](https://discord.gg/midjourney)

Return to top

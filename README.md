# Smart Word Filter — ComfyUI Prompt / Tag Toolkit

A small ComfyUI extension for organizing, filtering, and swapping prompt tags using reusable profiles. It ships with folder-based built-in tag lists (characters, clothing, pose, background, lighting, etc.) and lets you build your own positive / negative profiles once and reuse them in any workflow.

---

## What's inside

The extension adds two nodes:

| Node | Purpose |
| :--- | :--- |
| **Smart Word Filter** | The profile authoring hub. Create and save your own tag lists as reusable pos / neg profiles. |
| **Profile Tools (Split / Replace by Profile)** | Uses saved profiles to split a prompt into two groups, or replace some tags with others. Has a live, interactive preview. |

---

## Core concepts

* **Profiles:** A profile is just a named list of tags. Profiles are grouped into two kinds:
  * `pos`: Profiles you intend to use with your positive prompt.
  * `neg`: Profiles you intend to use with your negative prompt.
  * `pos` / `neg` is only a label to help you organize; both kinds work exactly the same way.
* **Built-in (★) profiles:** Profiles whose name starts with a star, such as `★ Face`, `★ Clothing`, `★ Pose`, are built automatically from text files on disk — they are not hard-coded. Because they are generic, they appear under both `pos` and `neg` (e.g. `pos | ★ Clothing` and `neg | ★ Clothing` are the same list).
* **Live update:** Edit a tag file (or add a new one) and the profiles refresh automatically — no need to restart ComfyUI.

---

## Node 1 — Smart Word Filter (profile authoring)

Use this node to turn any set of tags into a saved profile:

1. Type or paste your tags.
2. Mark the ones you want to keep (positive) and the ones you don't (negative).
3. Save the result as a named profile under `pos` or `neg`.

Saved profiles live on disk (independent of the workflow), so they are available in every workflow and survive restarts.

---

## Node 2 — Profile Tools (Split / Replace by Profile)

One node with an operation switch:

### operation = split

* **output 1 (kept):** The input tags that are inside the selected profile(s).
* **output 2 (rest):** Everything else.

In the node, every tag chip has two buttons:
* `+` = **want (force-keep):** Push this tag into output 1 even if it isn't in the profile.
* `-` = **don't want (force-remove):** Push this tag into output 2 even if it is in the profile.
* Click again to reset. "don't want" wins over "want".

### operation = replace

Removes the profile tags from the input and inserts your replacement tags in their place.
* **output 1 (result):** The resulting prompt.
* **output 2 (removed_tags):** The tags that were removed.
* `insert_at`: Controls where the replacement goes (at the first match, at the start, or at the end).
* `if_no_match`: Controls what to do when none of the profile tags were found (append / prepend / skip).

### mode (both operations)

* `any_profile`: A tag matches if it is in at least one selected profile (union).
* `all_profiles`: A tag matches only if it is in every selected profile (intersection).
* You can select up to 4 profiles at once (`profile`, `profile_2`, `profile_3`, `profile_4`).

**Live preview:** The node previews the result instantly as you change anything — you don't have to run the whole workflow. If the text comes from another node, run the workflow once so the node knows the latest text, then the preview stays live.

---

## How to add / edit tags

### A) Add tags to a built-in (★) list
1. Open the extension's `tag_lists/` sub-folder (it is created automatically after the first run).
2. Open the file for that category, e.g. `clothing.txt`.
3. Add your tag on a new line (one tag per line, or several separated by commas; lines starting with `#` are comments).
4. Save. The change applies live.

### B) Create a brand-new built-in category
Drop a new file like `animals.txt` into `tag_lists/` (or `tag_lists_default/`). A new `★ Animals` profile appears automatically.

### C) Create your own profile
Use the **Smart Word Filter** node, build your list, and save it under `pos` or `neg`. It will show up in the Profile Tools dropdown.

---

## Installation

1. Copy the `smart_word_filter` folder into `ComfyUI/custom_nodes/`.
2. Restart ComfyUI.
3. Hard-refresh the browser page (`Ctrl + F5`).

---

## Tips

* Tag matching ignores case and treats spaces / underscores the same (`blue_shirt` = `blue shirt`).
* Weights and brackets are handled, e.g. `(green:1.2)` is matched as `green`.
* Duplicate tags are removed automatically.

---
---

<div dir="rtl">

# راهنمای فارسی

### فیلتر هوشمند کلمات — ابزار پرامپت / تگ ComfyUI
یک افزونه کوچک برای ComfyUI جهت سازمان‌دهی، فیلتر کردن و جایگزینی تگ‌های پرامپت با استفاده از پروفایل‌های قابل استفاده مجدد. این افزونه به همراه لیست تگ‌های پیش‌فرض پوشه‌محور (شخصیت‌ها، لباس، فیگور/پوز، پس‌زمینه، نورپردازی و غیره) ارائه می‌شود و به شما امکان می‌دهد پروفایل‌های مثبت (Positive) / منفی (Negative) اختصاصی خود را یک‌بار بسازید و در هر ورک‌فلویی مجدداً استفاده کنید.

---

### محتویات افزونه
این افزونه دو نود (Node) اضافه می‌کند:

| نود | کاربرد |
| :--- | :--- |
| **Smart Word Filter** | مرکز ساخت و مدیریت پروفایل. لیست تگ‌های خود را بسازید و به عنوان پروفایل‌های مثبت/منفی قابل استفاده مجدد ذخیره کنید. |
| **Profile Tools (Split / Replace by Profile)** | از پروفایل‌های ذخیره‌شده برای جداسازی یک پرامپت به دو گروه یا جایگزینی برخی تگ‌ها با تگ‌های دیگر استفاده می‌کند. دارای پیش‌نمایش زنده و تعاملی است. |

---

### مفاهیم پایه

* **پروفایل‌ها (Profiles):** یک پروفایل صرفاً یک لیست نام‌گذاری‌شده از تگ‌هاست. پروفایل‌ها به دو دسته تقسیم می‌شوند:
  * `pos`: پروفایل‌هایی که قصد دارید در پرامپت مثبت استفاده کنید.
  * `neg`: پروفایل‌هایی که قصد دارید در پرامپت منفی استفاده کنید.
  * لیبل‌های `pos` / `neg` صرفاً برای کمک به سازمان‌دهی شما هستند؛ هر دو دسته دقیقاً به یک شکل عمل می‌کنند.
* **پروفایل‌های پیش‌فرض (★):** پروفایل‌هایی که نام آن‌ها با ستاره شروع می‌شود (مانند `★ Face`، `★ Clothing`، `★ Pose`) به صورت خودکار از فایل‌های متنی روی دیسک ساخته می‌شوند و هاردکد شده نیستند. از آنجا که عمومی هستند، هم در `pos` و هم در `neg` ظاهر می‌شوند (مثلاً `pos | ★ Clothing` و `neg | ★ Clothing` یک لیست واحد هستند).
* **به‌روزرسانی زنده (Live update):** یک فایل تگ را ویرایش کنید (یا فایل جدیدی اضافه کنید) تا پروفایل‌ها به طور خودکار بازخوانی شوند — نیازی به ری‌استارت کردن ComfyUI نیست.

---

### نود ۱ — Smart Word Filter (ساخت پروفایل)

از این نود برای تبدیل هر مجموعه‌ای از تگ‌ها به یک پروفایل ذخیره‌شده استفاده کنید:
1. تگ‌های خود را تایپ یا پیست (Paste) کنید.
2. تگ‌هایی که می‌خواهید نگه دارید (مثبت) و تگ‌هایی که نمی‌خواهید (منفی) را مشخص کنید.
3. نتیجه را به عنوان یک پروفایل نام‌گذاری‌شده زیر مجموعه `pos` یا `neg` ذخیره کنید.

پروفایل‌های ذخیره‌شده روی دیسک (مستقل از ورک‌فلو) قرار می‌گیرند؛ بنابراین در تمام ورک‌فلوها در دسترس بوده و با ری‌استارت برنامه‌ هم باقی می‌مانند.

---

### نود ۲ — Profile Tools (Split / Replace by Profile)

یک نود با یک کلید تغییر حالت (Operation Switch):

#### حالت split (جداسازی)
* **خروجی ۱ (kept):** تگ‌های ورودی که داخل پروفایل(های) انتخابی وجود دارند.
* **خروجی ۲ (rest):** بقیه تگ‌ها.

در داخل نود، هر کارت تگ (Tag chip) دارای دو دکمه است:
* `+` = **می‌خواهم (حفظ اجباری):** این تگ را وارد خروجی ۱ می‌کند، حتی اگر در پروفایل نباشد.
* `-` = **نمی‌خواهم (حذف اجباری):** این تگ را وارد خروجی ۲ می‌کند، حتی اگر در پروفایل باشد.
* کلیک مجدد باعث ریست شدن حالت می‌شود. حالت "نمی‌خواهم" بر حالت "می‌خواهم" اولویت دارد.

#### حالت replace (جایگزینی)
تگ‌های موجود در پروفایل را از ورودی حذف کرده و تگ‌های جایگزین شما را به جای آن‌ها وارد می‌کند.
* **خروجی ۱ (result):** پرامپت نهایی حاصل‌شده.
* **خروجی ۲ (removed_tags):** تگ‌هایی که حذف شده‌اند.
* `insert_at`: محل قرارگیری جایگزین را کنترل می‌کند (در اولین تطابق، در ابتدا، یا در انتها).
* `if_no_match`: تعیین می‌کند در صورت پیدا نشدن هیچ‌یک از تگ‌های پروفایل چه کاری انجام شود (افزودن به انتها / افزودن به ابتدا / صرف‌نظر کردن).

#### حالت mode (در هر دو عملیات)
* `any_profile`: اگر تگ حداقل در یکی از پروفایل‌های انتخابی باشد تطابق می‌یابد (اجتماع).
* `all_profiles`: تگ تنها در صورتی تطابق می‌یابد که در تمام پروفایل‌های انتخابی موجود باشد (اشتراک).
* می‌توانید هم‌زمان تا ۴ پروفایل انتخاب کنید (`profile`, `profile_2`, `profile_3`, `profile_4`).

**پیش‌نمایش زنده:** نود به محض تغییر هر پارامتر، نتیجه را فوراً پیش‌نمایش می‌دهد — نیازی به اجرای کامل ورک‌فلو نیست. اگر متن از نود دیگری می‌آید، ورک‌فلو را یک‌بار اجرا کنید تا نود آخرین متن را دریافت کند؛ پس از آن پیش‌نمایش به صورت زنده باقی می‌ماند.

---

### نحوه اضافه / ویرایش کردن تگ‌ها

**آ) اضافه کردن تگ به لیست پیش‌فرض (★)**
1. پوشه فرعی `tag_lists/` در افزونه را باز کنید (این پوشه پس از اولین اجرا به طور خودکار ساخته می‌شود).
2. فایل مربوط به آن دسته‌بندی را باز کنید (مثلاً `clothing.txt`).
3. تگ خود را در یک خط جدید اضافه کنید (هر خط یک تگ، یا چند تگ که با کاما از هم جدا شده‌اند؛ خطوطی که با `#` شروع می‌شوند کامنت هستند).
4. ذخیره کنید. تغییرات به صورت زنده اعمال می‌شوند.

**ب) ساخت یک دسته‌بندی پیش‌فرض کاملاً جدید**
یک فایل جدید مانند `animals.txt` را درون پوشه `tag_lists/` (یا `tag_lists_default/`) قرار دهید. پروفایل جدید `★ Animals` به صورت خودکار ظاهر می‌شود.

**پ) ساخت پروفایل اختصاصی خودتان**
از نود Smart Word Filter استفاده کنید، لیست خود را بسازید و آن را زیر مجموعه `pos` یا `neg` ذخیره کنید. این پروفایل در منوی کشویی Profile Tools نمایش داده خواهد شد.

---

### روش نصب

1. پوشه `smart_word_filter` را در مسیر `ComfyUI/custom_nodes/` کپی کنید.
2. برنامه ComfyUI را ری‌استارت کنید.
3. صفحه مرورگر را هارد ریفرش کنید (`Ctrl + F5`).

---

### نکات کاربردی
* بررسی تطابق تگ‌ها به بزرگ و کوچک بودن حروف حساس نیست و با فاصله (Space) و خط زیر (Underscore) یکسان رفتار می‌کند (`blue_shirt` = `blue shirt`).
* وزن‌ها و پرانتزها مدیریت می‌شوند؛ برای مثال `(green:1.2)` به عنوان `green` تطابق داده می‌شود.
* تگ‌های تکراری به صورت خودکار حذف می‌شوند.

</div>
<img width="1048" height="610" alt="Screenshot (1996)" src="https://github.com/user-attachments/assets/a3dc6f72-47cc-41e8-9fb3-4870b7ac3a57" />
<img width="1053" height="571" alt="Screenshot (1997)" src="https://github.com/user-attachments/assets/056bf4fd-645b-4266-a80d-ce164074885a" />

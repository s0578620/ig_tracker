import json
import time
import os
from datetime import datetime

def save_to_file(data, username, filename):
    """Speichert JSON-Daten in Benutzerordner/Datumsordner mit Datum im Dateinamen."""
    date_stamp = datetime.now().strftime("%Y%m%d")
    user_folder = os.path.join("data", username, date_stamp)
    os.makedirs(user_folder, exist_ok=True)
    full_path = os.path.join(user_folder, f"{date_stamp}_{filename}.json")
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Gespeichert: {full_path}")

def inject_and_fetch(driver, username):
    print("🚀 Vollautomatisches JavaScript Injection gestartet...")

    js_template = """
    var textarea = document.createElement('textarea');
    textarea.id = 'injector';
    textarea.style.display = 'none';
    textarea.textContent = `
    const username = "<<<USERNAME>>>";

    window.followers = [];
    window.followings = [];
    window.dontFollowMeBack = [];
    window.iDontFollowBack = [];

    (async () => {
      try {
        console.log('Process started! Give it a couple of seconds');

        const userQueryRes = await fetch(
          'https://www.instagram.com/web/search/topsearch/?query=' + username
        );
        const userQueryJson = await userQueryRes.json();
        const userId = userQueryJson.users.map(u => u.user).filter(u => u.username === username)[0].pk;

        let after = null;
        let has_next = true;

        while (has_next) {
          const res = await fetch(
            'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=' +
            encodeURIComponent(JSON.stringify({
              id: userId,
              include_reel: true,
              fetch_mutual: true,
              first: 50,
              after: after,
            }))
          );
          const json = await res.json();
          has_next = json.data.user.edge_followed_by.page_info.has_next_page;
          after = json.data.user.edge_followed_by.page_info.end_cursor;
          window.followers = window.followers.concat(
            json.data.user.edge_followed_by.edges.map(({ node }) => ({
              id: node.id,   
              username: node.username,
              full_name: node.full_name,
              is_verified: node.is_verified,
              is_private: node.is_private,
              profile_pic_url: node.profile_pic_url
            }))
          );
        }

        console.log({ followers: window.followers });

        after = null;
        has_next = true;

        while (has_next) {
          const res = await fetch(
            'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=' +
            encodeURIComponent(JSON.stringify({
              id: userId,
              include_reel: true,
              fetch_mutual: true,
              first: 50,
              after: after,
            }))
          );
          const json = await res.json();
          has_next = json.data.user.edge_follow.page_info.has_next_page;
          after = json.data.user.edge_follow.page_info.end_cursor;
          window.followings = window.followings.concat(
            json.data.user.edge_follow.edges.map(({ node }) => ({
              id: node.id,
              username: node.username,
              full_name: node.full_name,
              is_verified: node.is_verified,
              is_private: node.is_private,
              profile_pic_url: node.profile_pic_url
            }))
          );
        }

        console.log({ followings: window.followings });

        window.dontFollowMeBack = window.followings.filter((following) => {
          return !window.followers.find((follower) => follower.username === following.username);
        });

        console.log({ dontFollowMeBack: window.dontFollowMeBack });

        window.iDontFollowBack = window.followers.filter((follower) => {
          return !window.followings.find((following) => following.username === follower.username);
        });

        console.log({ iDontFollowBack: window.iDontFollowBack });

        console.log('Process done! Type copy(followers) etc.');
      } catch (err) {
        console.log({ err });
      }
    })();
    `;
    document.body.appendChild(textarea);
    eval(document.getElementById('injector').textContent);
    """

    js_code = js_template.replace("<<<USERNAME>>>", username)
    driver.execute_script(js_code)

    print("⏳ JavaScript erfolgreich vollautomatisch gestartet!")
    time.sleep(60)  # Warten bis API fertig

    # Jetzt Daten holen:
    followers = driver.execute_script("return window.followers;")
    followings = driver.execute_script("return window.followings;")
    dontFollowMeBack = driver.execute_script("return window.dontFollowMeBack;")
    iDontFollowBack = driver.execute_script("return window.iDontFollowBack;")

    print(f"✅ Followers geladen: {len(followers)} Stück")
    print(f"✅ Followings geladen: {len(followings)} Stück")
    print(f"✅ Nicht zurückgefolgt: {len(dontFollowMeBack)} Stück")
    print(f"✅ Ich folge nicht zurück: {len(iDontFollowBack)} Stück")

    # Speichern
    save_to_file(followers, username, "followers")
    save_to_file(followings, username, "followings")
    save_to_file(dontFollowMeBack, username, "dontFollowMeBack")
    save_to_file(iDontFollowBack, username, "iDontFollowBack")
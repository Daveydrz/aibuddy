import json
import os
from datetime import datetime

def load_voice_data():
    """Load voice profiles data"""
    try:
        file_path = "voice_profiles/known_users_v2.json"
        with open(file_path, 'r') as f:
            return json.load(f), file_path
    except FileNotFoundError:
        print(f"❌ File not found: voice_profiles/known_users_v2.json")
        return None, None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON format in file")
        return None, None
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None, None

def create_backup(data, file_path):
    """Create backup before deletion"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"voice_profiles/backup_{timestamp}.json"
        
        with open(backup_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return None

def save_voice_data(data, file_path):
    """Save updated voice data"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Data saved successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to save data: {e}")
        return False

def display_profiles(data):
    """Display all available profiles"""
    known_users = data.get('known_users', {})
    anonymous_clusters = data.get('anonymous_clusters', {})
    
    print(f"\n" + "="*60)
    print(f"🔍 AVAILABLE VOICE PROFILES")
    print(f"📅 Current time: 2025-07-14 10:04:11 UTC")
    print(f"👤 User: Daveydrz")
    print(f"="*60)
    
    all_profiles = []
    
    # Known Users
    if known_users:
        print(f"\n📊 KNOWN USERS ({len(known_users)}):")
        for i, (user_id, user_data) in enumerate(known_users.items(), 1):
            name = user_data.get('name', user_id)
            embedding_count = len(user_data.get('embeddings', []))
            created = user_data.get('created_date', 'Unknown')
            status = user_data.get('status', 'Unknown')
            
            print(f"  {i:2d}. {user_id}")
            print(f"      Name: {name}")
            print(f"      Voice samples: {embedding_count}")
            print(f"      Status: {status}")
            print(f"      Created: {created}")
            print()
            
            all_profiles.append(('known_user', user_id, user_data))
    else:
        print(f"\n📊 KNOWN USERS: None")
    
    # Anonymous Clusters
    if anonymous_clusters:
        print(f"📊 ANONYMOUS CLUSTERS ({len(anonymous_clusters)}):")
        start_num = len(known_users) + 1
        
        for i, (cluster_id, cluster_data) in enumerate(anonymous_clusters.items(), start_num):
            cluster_name = cluster_data.get('test_name', 'Unnamed')
            embedding_count = len(cluster_data.get('embeddings', []))
            created = cluster_data.get('created_at', 'Unknown')
            status = cluster_data.get('status', 'anonymous')
            
            print(f"  {i:2d}. {cluster_id}")
            print(f"      Name: {cluster_name}")
            print(f"      Voice samples: {embedding_count}")
            print(f"      Status: {status}")
            print(f"      Created: {created}")
            print()
            
            all_profiles.append(('anonymous_cluster', cluster_id, cluster_data))
    else:
        print(f"📊 ANONYMOUS CLUSTERS: None")
    
    return all_profiles

def get_user_choice(all_profiles):
    """Get user's deletion choice"""
    if not all_profiles:
        print(f"❌ No profiles available to delete")
        return None
    
    print(f"\n" + "="*60)
    print(f"🗑️ DELETION OPTIONS:")
    print(f"   0. Cancel - Don't delete anything")
    
    for i, (profile_type, profile_id, profile_data) in enumerate(all_profiles, 1):
        if profile_type == 'known_user':
            name = profile_data.get('name', profile_id)
            print(f"   {i}. Delete known user: {profile_id} ({name})")
        else:
            name = profile_data.get('test_name', 'Unnamed')
            print(f"   {i}. Delete anonymous cluster: {profile_id} ({name})")
    
    print(f"  99. Delete ALL profiles (⚠️ DANGEROUS!)")
    print(f"="*60)
    
    while True:
        try:
            choice = input(f"\nEnter your choice (0-{len(all_profiles)} or 99): ").strip()
            
            if choice == "0":
                return None
            elif choice == "99":
                return "DELETE_ALL"
            else:
                choice_num = int(choice)
                if 1 <= choice_num <= len(all_profiles):
                    return all_profiles[choice_num - 1]
                else:
                    print(f"❌ Invalid choice. Please enter 0-{len(all_profiles)} or 99")
        except ValueError:
            print(f"❌ Please enter a valid number")

def confirm_deletion(selection):
    """Confirm deletion with user"""
    if selection == "DELETE_ALL":
        print(f"\n⚠️ WARNING: You are about to DELETE ALL VOICE PROFILES!")
        print(f"This will permanently remove:")
        print(f"  • All known users")
        print(f"  • All anonymous clusters")
        print(f"  • All voice samples and embeddings")
        print(f"\nThis action CANNOT BE UNDONE!")
        
        confirm = input(f"\nType 'DELETE ALL PROFILES' to confirm: ").strip()
        return confirm == "DELETE ALL PROFILES"
    else:
        profile_type, profile_id, profile_data = selection
        
        if profile_type == 'known_user':
            name = profile_data.get('name', profile_id)
            print(f"\n⚠️ You are about to delete known user: {profile_id} ({name})")
        else:
            name = profile_data.get('test_name', 'Unnamed')
            print(f"\n⚠️ You are about to delete anonymous cluster: {profile_id} ({name})")
        
        embedding_count = len(profile_data.get('embeddings', []))
        print(f"This will permanently remove {embedding_count} voice samples.")
        
        confirm = input(f"\nType 'YES' to confirm deletion: ").strip().upper()
        return confirm == "YES"

def delete_profile(data, selection):
    """Delete the selected profile"""
    if selection == "DELETE_ALL":
        data['known_users'] = {}
        data['anonymous_clusters'] = {}
        print(f"✅ All profiles deleted from memory")
        return True
    else:
        profile_type, profile_id, profile_data = selection
        
        if profile_type == 'known_user':
            if profile_id in data['known_users']:
                del data['known_users'][profile_id]
                print(f"✅ Deleted known user: {profile_id}")
                return True
            else:
                print(f"❌ Known user not found: {profile_id}")
                return False
        else:
            if profile_id in data['anonymous_clusters']:
                del data['anonymous_clusters'][profile_id]
                print(f"✅ Deleted anonymous cluster: {profile_id}")
                return True
            else:
                print(f"❌ Anonymous cluster not found: {profile_id}")
                return False

def main():
    """Main function"""
    print(f"🗑️ VOICE PROFILE DELETION TOOL")
    print(f"📅 Current time: 2025-07-14 10:04:11 UTC")
    print(f"👤 User: Daveydrz")
    
    # Load data
    data, file_path = load_voice_data()
    if data is None:
        return
    
    # Display profiles
    all_profiles = display_profiles(data)
    
    if not all_profiles:
        print(f"\n❌ No profiles found to delete")
        return
    
    # Get user choice
    selection = get_user_choice(all_profiles)
    if selection is None:
        print(f"\n✅ Deletion cancelled")
        return
    
    # Confirm deletion
    if not confirm_deletion(selection):
        print(f"\n✅ Deletion cancelled")
        return
    
    # Create backup
    backup_path = create_backup(data, file_path)
    if backup_path is None:
        print(f"\n❌ Cannot proceed without backup")
        return
    
    # Delete profile
    success = delete_profile(data, selection)
    if not success:
        print(f"\n❌ Deletion failed")
        return
    
    # Save updated data
    if save_voice_data(data, file_path):
        print(f"\n🎉 SUCCESS!")
        print(f"✅ Profile(s) deleted successfully")
        print(f"💾 Backup saved: {backup_path}")
        print(f"💡 Restart your voice system to apply changes")
        
        # Show remaining profiles
        remaining_known = len(data.get('known_users', {}))
        remaining_anonymous = len(data.get('anonymous_clusters', {}))
        print(f"\n📊 Remaining profiles:")
        print(f"  • Known users: {remaining_known}")
        print(f"  • Anonymous clusters: {remaining_anonymous}")
    else:
        print(f"\n❌ Failed to save changes")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n✅ Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
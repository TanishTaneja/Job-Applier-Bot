# import os
# import shutil

# current_dir = os.getcwd()

# for item in os.listdir(current_dir):
#     item_path = os.path.join(current_dir, item)
    
#     try:
#         if os.path.isfile(item_path) or os.path.islink(item_path):
#             os.remove(item_path)
#         elif os.path.isdir(item_path):
#             shutil.rmtree(item_path)
#     except Exception as e:
#         print(f"Error deleting {item_path}: {e}")
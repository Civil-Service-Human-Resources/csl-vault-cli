import argparse
import getpass
import sys
import add
import update
import delete
import bulk
import load
from Validation import Validation

def main():
    try:
        action = sys.argv[1]
        args = get_arguments(action)

        validate_arguments(args)
        
        if hasattr(args, "value") and args.value == None:
            args.value = getpass.getpass(f"Enter value for variable '{args.name}': ")

        run_action(args)
    except ValueError as ve:
        print(f"❌ {ve}")

def get_arguments(action):
    parser = argparse.ArgumentParser()
    validation = Validation()

    parser.add_argument("action")

    if action in ["add", "update", "delete"]:
        
        parser.add_argument("environment")
        parser.add_argument("module")
        parser.add_argument("name")

    if action == "add":
        parser.add_argument("--secret", help="Secret", action=argparse.BooleanOptionalAction)

    if action in ["add", "update"]:
        parser.add_argument("--value", help="Value of secret")

    if action == "bulk-add":
        parser.add_argument("file_path")

    if action == "load":
        parser.add_argument("environment")

    args = parser.parse_args()
    return args

def validate_arguments(args):
    validation = Validation()
    validation.validate_action(args.action)
    if hasattr(args, "environment"):
        validation.validate_environment(args.environment) 
    if hasattr(args, "module"):
        validation.validate_module(args.module)
    if hasattr(args, "name"):
        validation.validate_variable(args.action, args.environment, args.module, args.name)

def run_action(args):
    if args.action == "add":    
        add.add_var(args.environment, args.module, args.name, args.value, True if args.secret else False)

    elif args.action == "update":
        update.update_var(args)

    elif args.action == "delete":
        delete.delete_var(args)

    elif args.action == "bulk-add":
        bulk.add(args.file_path)

    elif args.action == "load":
        load.load(args.environment)

if __name__ == "__main__":
    main()
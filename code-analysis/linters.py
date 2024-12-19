from pylint.lint import Run
import subprocess
from os import listdir


def code_analysis(file):
    list_files = listdir(file)
    
    for file in list_files:
        file = './unzipped_files/'+file

        if file.endswith('.py'):
            # pylint_fail_under
            results = Run([file], exit=False)

            error=results.linter.stats.error
            warning=results.linter.stats.warning
            print(f"No. of Errors:{error}\nNo. of Warning:{warning}")

        elif file.endswith(('.c','.cc','.cpp','.c++','.h','.hpp','.h++','cu','cuh','cxx','hxx')):

            try:
                result = subprocess.run(
                    ['cpplint',"--counting=detailed", file],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                print(f"Errors Encountered:\n{result.stderr}")
                print(result.stdout)
                
            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n{e.stderr}")
                print(e.output)

        elif file.endswith('.java'):
            def parse_checkstyle_output(output):
                warning = 0
                error = 0

                for line in output.splitlines():
                    if "[WARN]" in line:
                        warning+=1
                    elif "[ERROR]" in line:
                        error+=1

                return warning,error
            try:
                result = subprocess.run(
                    ['checkstyle', file],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                
                if result.stdout:
                    print(result.stdout)
                    print(f"Warnings:{parse_checkstyle_output(result.stdout)[0]}")
                    print(f"Warnings:{parse_checkstyle_output(result.stdout)[1]}")
                
                if result.stderr:
                    print(result.stderr)
                    

            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n {e.output}")
                print(f"Warnings:{parse_checkstyle_output(e.stdout)[0]}")
                print(f"Warnings:{parse_checkstyle_output(e.stdout)[1]}")

        elif file.endswith(('.yaml','.yml')):
            def parse_yamllint_output(output):
                score=0
                warning = 0
                error = 0

                for line in output.splitlines():
                    if "warning" in line:
                        warning+=1
                    elif "error" in line:
                        error+=1

                return warning,error
            try:
                result = subprocess.run(
                    ['yamllint', file],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                if result.stdout:
                    print(result.stdout)
                    print(f"Warnings:{parse_yamllint_output(result.stdout)[0]}")
                    print(f"Errors:{parse_yamllint_output(result.stdout)[1]}")
                
                if result.stderr:
                    print('sdad')
                    print(result.stderr)
                
            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n {e.output}")
                print(f"Warnings:{parse_yamllint_output(e.stdout)[0]}")
                print(f"Errors:{parse_yamllint_output(e.stdout)[1]}")

        elif file.endswith('.sql'):
            def sqlfluff_output(output):
                warning = 0

                for line in output.splitlines():
                    if "L" in line:
                        warning+=1
                
                return warning            

            try:
                dialect = 'mysql'
                result = subprocess.run(
                    ['sqlfluff','lint',file,'--dialect', dialect],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                if result.stdout:
                    print(result.stdout)
                    print(sqlfluff_output(result.stdout))
                
                if result.stderr:
                    print(result.stderr)
                
            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n{e.output}")
                print(f"Number of Warnings:{sqlfluff_output(e.stdout)}")

        elif file.endswith('.css'):

            def countsError(output):
                # Initialize error and warning counters
                num_errors = 0
                num_warnings = 0

                # Parse the output for errors and warnings
                for line in output.splitlines():
                    if 'error' in line:
                        num_errors += 1
                    elif 'warning' in line:
                        num_warnings += 1
                
                return num_errors,num_warnings

            try:
                result = subprocess.run(
                    ['csslint',file,],
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True
                )
                if result.stdout:
                    print(result.stdout)
                    print(f"Number of errors:{countsError(result.stdout)[0]}\nNumber of warnings:{countsError(result.stdout)[1]}")
                
                if result.stderr:
                    print(result.stderr)
                
            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n {e.output}")
                print(f"Number of errors:{countsError(e.stdout)[0]}\nNumber of warnings:{countsError(e.stdout)[1]}")

        elif file.endswith(('.js','ts')):

            try:
                result = subprocess.run(
                    ['npx','eslint',file,],
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True
                )

                if result.stdout:
                    print(result.stdout)
                
                if result.stderr:
                    print(result.stderr)
                
            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n {e.output}")

        elif file.endswith('.sh'):
            def countsError(output):
                # Initialize error and warning counters
                num_errors = 0
                num_warnings = 0

                # Parse the output for errors and warnings
                for line in output.splitlines():
                    if 'error' in line:
                        num_errors += 1
                    elif 'warning' in line:
                        num_warnings += 1
                
                return num_errors,num_warnings

            try:
                result = subprocess.run(
                    ['shellcheck',file,],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                if result.stdout:
                    print(result.stdout)
                    print(f"Number of errors:{countsError(result.stdout)[0]}\nNumber of warnings:{countsError(result.stdout)[1]}")

                
                if result.stderr:
                    print(result.stderr)
                
            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n {e.output}")
                print(f"Number of errors:{countsError(e.stdout)[0]}\nNumber of warnings:{countsError(e.stdout)[1]}")

        elif file.endswith('.html'):

            try:           
                    # Command to be executed
                    command = ['tidy', file]
                    
                    # Run the command
                    result = subprocess.run(command, capture_output=True, text=True, check=True)
                    
                    # Print any errors encountered
                    if result.stderr:
                        print("Standard Error:")
                        print(result.stderr)
                    
            except subprocess.CalledProcessError as e:
                    print(f"An error occurred while running htmlcheck: {e.stderr}")

        elif file.endswith('.json'):

            try:
                result = subprocess.run(
                    ['jsonlint',file,],
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True
                )
                
                if result.stderr:
                    print(result.stderr)
                
            except subprocess.CalledProcessError as e:
                print(f"Errors Encountered:\n {e.stderr}")




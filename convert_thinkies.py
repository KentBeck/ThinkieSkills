import os
import re
import yaml
from bs4 import BeautifulSoup

def parse_filename(filename):
    # Remove ID prefix and extension
    # e.g. 147932285.thinkie-explore-or-extract.html -> thinkie-explore-or-extract
    base = filename.split('.', 1)[1].rsplit('.', 1)[0]
    
    # Remove 'thinkie-' prefix if present
    if base.startswith('thinkie-'):
        base = base[8:]
    
    # Replace hyphens with underscores for ID
    thinkie_id = base.replace('-', '_')
    
    # Create readable name
    name = base.replace('-', ' ').title()
    
    return thinkie_id, name

def extract_content(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    pattern = ""
    transformation = ""
    trigger = ""
    body = []
    
    for line in lines:
        if line.startswith("Pattern:"):
            pattern = line.replace("Pattern:", "").strip()
        elif line.startswith("Transformation:"):
            transformation = line.replace("Transformation:", "").strip()
        elif line.startswith("Trigger:"):
            trigger = line.replace("Trigger:", "").strip()
        else:
            body.append(line)
            
    return {
        "pattern": pattern,
        "transformation": transformation,
        "trigger": trigger,
        "body": "\n".join(body)
    }

def generate_yaml(thinkie_id, name, content):
    # Heuristics for fields
    intent = content["transformation"] if content["transformation"] else f"Help you with {name}."
    
    triggers = []
    if content["trigger"]:
        triggers.append(content["trigger"])
    if content["pattern"]:
        triggers.append(content["pattern"][:50] + "...") # Truncate if too long
    if not triggers:
        triggers.append(name.lower())
        
    preconditions = []
    if content["pattern"]:
        preconditions.append(content["pattern"])
    else:
        preconditions.append(f"You are interested in {name}.")
        
    # Find questions in body
    questions = []
    for line in content["body"].split('\n'):
        if '?' in line:
            # Simple heuristic: take the sentence ending in ?
            # This is rough, but better than nothing
            parts = line.split('?')
            for part in parts:
                if len(part.strip()) > 10 and len(part.strip()) < 150:
                    questions.append({
                        "id": "q_" + str(len(questions)),
                        "prompt": part.strip() + "?"
                    })
            if len(questions) >= 3:
                break
    
    if not questions:
        questions.append({
            "id": "situation",
            "prompt": "What is the situation you are facing?"
        })

    yaml_content = {
        "id": thinkie_id,
        "name": name,
        "intent": intent,
        "triggers": triggers,
        "preconditions": preconditions,
        "voice": {
            "style": "analytical",
            "tone": "helpful"
        },
        "questions": questions,
        "scaffold": {
            "guidance": f"The user is facing this pattern: {content['pattern']}.\nYour goal is to help them apply this transformation: {content['transformation']}.\n\nContext:\n{content['body'][:500]}..."
        },
        "output_template": f"Pattern: {content['pattern']}\nTransformation: {content['transformation']}\n\nAnalysis:\n{{analysis}}\n\nSuggested Next Step:\n{{next_step}}",
        "examples": [],
        "pitfalls": []
    }
    
    return yaml_content

def main():
    input_dir = "thinkie_htmls"
    output_dir = "thinkies"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(input_dir):
        if not filename.endswith(".html"):
            continue
            
        thinkie_id, name = parse_filename(filename)
        html_path = os.path.join(input_dir, filename)
        
        # Skip if YAML already exists (don't overwrite pilot batch)
        yaml_path = os.path.join(output_dir, f"{thinkie_id}.yaml")
        if os.path.exists(yaml_path):
            print(f"Skipping existing: {yaml_path}")
            continue
            
        try:
            content = extract_content(html_path)
            yaml_data = generate_yaml(thinkie_id, name, content)
            
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, sort_keys=False, allow_unicode=True, width=1000)
                
            print(f"Generated: {yaml_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()

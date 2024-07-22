import json

class Templates:
    def __init__(self, agent_path: str, task_path: str) -> None:
        self.section_tpl = {}
        self.task_json = {}

        with open(agent_path, 'r') as f:
            data = json.load(f)
        self.researcher = data['researcher']['system_prompt']
        self.writer = data['writer']['system_prompt']
        
        with open(task_path, 'r') as f:
            self.task_json = json.load(f)
        
        for row in self.task_json:
            section_sys_prompt = 'Here are some instructions on how to fill out this section.'
            section_sys_prompt += f"\nSection: {row['section'].strip('<[]>')}"
            section_sys_prompt += f"\nInstructions: {row['special_instructions']}"
            section_sys_prompt += f"\nExpected Output: {row['expected_output']}"
            self.section_tpl[row['section']] = section_sys_prompt
        
    def get_sec_tpl(self, key: str) -> str:
        if (not key.startswith('<[')) and (not key.endswith(']>')):
            key = f'<[{key}]>'
        return self.section_tpl[key]
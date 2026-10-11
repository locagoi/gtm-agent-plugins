"""Offline checks for reusable goal/setup instructions, without customer fixtures."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1] / 'gtm/skills'

class AutonomyContract(unittest.TestCase):
    def test_goal_recipe_uses_current_tools_and_retains_release_gates(self):
        text = (ROOT/'agents-loops-goals/SKILL.md').read_text()
        for obsolete in ['gtm call create_mission', 'gtm call get_mission', 'Never automate a judgement you have not watched a human make twenty times']:
            self.assertNotIn(obsolete, text)
        for contract in ['get_goal_plan', 'full_gtm_chain', 'first send', 'budget', 'legal', 'delet', 'scal', 'unclear']:
            self.assertIn(contract, text)
        self.assertIn('no tool named get_goal_plan', text)

    def test_setup_verifies_existing_connection_before_requesting_credentials(self):
        text = (ROOT/'setup/SKILL.md').read_text()
        self.assertIn('Step 0', text)
        self.assertLess(text.index('gtm whoami'), text.index('## Step 1'))
        self.assertNotIn('Stop and ask the user for anything', text)
        self.assertIn('Never print', text)
        self.assertIn('genuinely missing', text)

    def test_intake_uses_evidence_before_a_missing_input_interview(self):
        for skill in ['gtm-quickstart', 'draft-gtm-play']:
            text = (ROOT/skill/'SKILL.md').read_text()
            self.assertIn('derive before asking', text)
            self.assertIn('assumption', text)

if __name__ == '__main__':
    unittest.main()

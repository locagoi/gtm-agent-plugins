"""Offline checks for the closed-loop skills: present, single-workspace, gated, generic."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'gtm/skills'
LOOP = ['closed-loop', 'health-check', 'sourcing-topup', 'enroll-outreach', 'reply-triage',
        'deliverability', 'optimize-outreach', 'playbook-from-winners']


def read(skill):
    return (ROOT / skill / 'SKILL.md').read_text()


def flat(skill):
    return ' '.join(read(skill).lower().split())


class ClosedLoopSkills(unittest.TestCase):
    def test_each_skill_has_matching_frontmatter(self):
        for skill in LOOP:
            text = read(skill)
            self.assertTrue(text.startswith('---\n'), skill)
            self.assertIn(f'\nname: {skill}\n', text.split('\n---', 1)[0] + '\n', skill)
            self.assertIn('\ndescription: ', text, skill)

    def test_entry_point_routes_to_every_station(self):
        text = read('closed-loop')
        for skill in LOOP[1:]:
            self.assertIn(f'`{skill}`', text)
        for rule in ['Read freely, write only after confirmation', 'No automatic retries',
                     'not proof of sending', 'Never invent']:
            self.assertIn(rule, text)

    def test_stations_point_back_to_the_shared_rules(self):
        for skill in LOOP[1:]:
            self.assertIn('`closed-loop`', read(skill), skill)

    def test_one_workspace_no_fan_out(self):
        for skill in LOOP:
            text = read(skill)
            self.assertNotRegex(text, r'mcp__gtm-', skill)
            self.assertNotIn('<slug>', text, skill)
            self.assertNotRegex(text.lower(), r'all workspaces|across workspaces|cross-workspace (?!patterns)', skill)

    def test_mutating_stations_keep_their_gate(self):
        for skill in ['sourcing-topup', 'enroll-outreach', 'reply-triage', 'deliverability',
                      'playbook-from-winners']:
            self.assertRegex(flat(skill), r'explicit yes|wait(s|ing)? for (a|your|an explicit) yes', skill)
        self.assertIn('changes nothing', flat('optimize-outreach'))
        self.assertIn('never mutates', flat('health-check'))

    def test_no_hardcoded_ids_paths_or_secrets(self):
        uuid = re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b')
        for skill in LOOP:
            text = read(skill)
            self.assertIsNone(uuid.search(text), skill)
            self.assertNotRegex(text, r'/home/|~/|mcp_[A-Za-z0-9]{16,}', skill)


if __name__ == '__main__':
    unittest.main()

import sqlite3
import json

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('agents.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create agents table with expanded schema
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            expertise TEXT NOT NULL,
            description TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
        ''')

        # Create table for agent prompts
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER NOT NULL,
            prompt_template TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
        ''')

        # Create table for agent parameters
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER NOT NULL,
            param_name TEXT NOT NULL,
            param_type TEXT NOT NULL,
            is_required BOOLEAN DEFAULT TRUE,
            description TEXT,
            default_value TEXT,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
        ''')

        # Create table for agent configurations
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER NOT NULL,
            config_key TEXT NOT NULL,
            config_value TEXT NOT NULL,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
        ''')

        self.conn.commit()

    def create_agent(self, agent_data):
        try:
            # Start a transaction
            self.conn.execute('BEGIN')

            # Insert agent basic information
            self.cursor.execute('''
            INSERT INTO agents (name, expertise, description, agent_type)
            VALUES (?, ?, ?, ?)
            ''', (
                agent_data['name'],
                agent_data['expertise'],
                agent_data['description'],
                agent_data['agent_type']
            ))
            agent_id = self.cursor.lastrowid

            # Insert agent prompt
            self.cursor.execute('''
            INSERT INTO agent_prompts (agent_id, prompt_template)
            VALUES (?, ?)
            ''', (agent_id, agent_data['prompt']))

            # Insert agent parameters
            params = agent_data['required_params'].split(',')
            for param in params:
                param = param.strip()
                self.cursor.execute('''
                INSERT INTO agent_parameters (agent_id, param_name, param_type, is_required)
                VALUES (?, ?, ?, ?)
                ''', (agent_id, param, 'string', True))

            # Insert any additional configurations
            if 'configs' in agent_data:
                for key, value in agent_data['configs'].items():
                    self.cursor.execute('''
                    INSERT INTO agent_configs (agent_id, config_key, config_value)
                    VALUES (?, ?, ?)
                    ''', (agent_id, key, json.dumps(value)))

            # Commit the transaction
            self.conn.commit()
            return agent_id

        except Exception as e:
            self.conn.rollback()
            raise e

    def get_agents(self):
        """Get all active agents with their prompts and parameters"""
        self.cursor.execute('''
        SELECT 
            a.id,
            a.name,
            a.expertise,
            a.description,
            a.agent_type,
            ap.prompt_template,
            GROUP_CONCAT(param.param_name) as parameters
        FROM agents a
        LEFT JOIN agent_prompts ap ON ap.agent_id = a.id AND ap.is_active = TRUE
        LEFT JOIN agent_parameters param ON param.agent_id = a.id
        WHERE a.is_active = TRUE
        GROUP BY a.id
        ''')
        return self.cursor.fetchall()

    def get_agent_details(self, agent_id):
        """Get detailed information about a specific agent"""
        # Get basic agent info
        self.cursor.execute('''
        SELECT * FROM agents WHERE id = ? AND is_active = TRUE
        ''', (agent_id,))
        agent = self.cursor.fetchone()

        if not agent:
            return None

        # Get current prompt
        self.cursor.execute('''
        SELECT prompt_template FROM agent_prompts 
        WHERE agent_id = ? AND is_active = TRUE 
        ORDER BY version DESC LIMIT 1
        ''', (agent_id,))
        prompt = self.cursor.fetchone()

        # Get parameters
        self.cursor.execute('''
        SELECT param_name, param_type, is_required, description, default_value 
        FROM agent_parameters WHERE agent_id = ?
        ''', (agent_id,))
        parameters = self.cursor.fetchall()

        # Get configurations
        self.cursor.execute('''
        SELECT config_key, config_value FROM agent_configs WHERE agent_id = ?
        ''', (agent_id,))
        configs = self.cursor.fetchall()

        return {
            'agent': agent,
            'prompt': prompt[0] if prompt else None,
            'parameters': parameters,
            'configs': {k: json.loads(v) for k, v in configs} if configs else {}
        }

    def update_agent(self, agent_id, agent_data):
        try:
            self.conn.execute('BEGIN')

            # Update basic agent information
            self.cursor.execute('''
            UPDATE agents 
            SET name=?, expertise=?, description=?, agent_type=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            ''', (
                agent_data['name'],
                agent_data['expertise'],
                agent_data['description'],
                agent_data['agent_type'],
                agent_id
            ))

            # Update prompt - create new version
            self.cursor.execute('''
            UPDATE agent_prompts SET is_active = FALSE 
            WHERE agent_id = ? AND is_active = TRUE
            ''', (agent_id,))

            self.cursor.execute('''
            INSERT INTO agent_prompts (agent_id, prompt_template, version)
            SELECT ?, ?, COALESCE(MAX(version), 0) + 1
            FROM agent_prompts WHERE agent_id = ?
            ''', (agent_id, agent_data['prompt'], agent_id))

            # Update parameters
            self.cursor.execute('DELETE FROM agent_parameters WHERE agent_id = ?', (agent_id,))
            params = agent_data['required_params'].split(',')
            for param in params:
                param = param.strip()
                self.cursor.execute('''
                INSERT INTO agent_parameters (agent_id, param_name, param_type, is_required)
                VALUES (?, ?, ?, ?)
                ''', (agent_id, param, 'string', True))

            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e

    def delete_agent(self, agent_id):
        """Soft delete an agent"""
        try:
            self.cursor.execute('''
            UPDATE agents SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (agent_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting agent: {e}")
            return False

    def __del__(self):
        self.conn.close()
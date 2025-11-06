-- Network Pinpointer PostgreSQL Schema
-- Stores network flows, analysis results, and LJPW history

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- ============================================================================
-- FLOWS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS flows (
    -- Identity
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    flow_id VARCHAR(255) UNIQUE NOT NULL,

    -- Network metadata
    src_ip VARCHAR(45) NOT NULL,  -- IPv4 or IPv6
    dst_ip VARCHAR(45) NOT NULL,
    src_port INTEGER,
    dst_port INTEGER,
    protocol VARCHAR(10) NOT NULL,  -- TCP, UDP, ICMP, etc.

    -- Semantic classification
    dominant_intent VARCHAR(50) NOT NULL,  -- CONNECTION_ESTABLISHMENT, AUTHENTICATION, etc.
    flow_pattern VARCHAR(100),  -- Known pattern name if matched

    -- LJPW coordinates (aggregate for entire flow)
    love DECIMAL(3,2) NOT NULL CHECK (love >= 0 AND love <= 1),
    justice DECIMAL(3,2) NOT NULL CHECK (justice >= 0 AND justice <= 1),
    power DECIMAL(3,2) NOT NULL CHECK (power >= 0 AND power <= 1),
    wisdom DECIMAL(3,2) NOT NULL CHECK (wisdom >= 0 AND wisdom <= 1),

    -- Anomaly detection
    anomaly_score DECIMAL(3,2) NOT NULL DEFAULT 0.0 CHECK (anomaly_score >= 0 AND anomaly_score <= 1),
    anomaly_reasons TEXT[],  -- Array of reasons why flagged as anomalous
    is_suspicious BOOLEAN DEFAULT false,

    -- Flow statistics
    packet_count INTEGER DEFAULT 0,
    byte_count BIGINT DEFAULT 0,
    duration_seconds DECIMAL(10,2),

    -- Timestamps
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Indexing
    CONSTRAINT valid_ports CHECK (
        (src_port IS NULL OR (src_port >= 0 AND src_port <= 65535)) AND
        (dst_port IS NULL OR (dst_port >= 0 AND dst_port <= 65535))
    )
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_flows_started_at ON flows(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_flows_dst_ip ON flows(dst_ip);
CREATE INDEX IF NOT EXISTS idx_flows_src_ip ON flows(src_ip);
CREATE INDEX IF NOT EXISTS idx_flows_dominant_intent ON flows(dominant_intent);
CREATE INDEX IF NOT EXISTS idx_flows_anomaly_score ON flows(anomaly_score DESC) WHERE anomaly_score > 0.7;
CREATE INDEX IF NOT EXISTS idx_flows_suspicious ON flows(is_suspicious) WHERE is_suspicious = true;
CREATE INDEX IF NOT EXISTS idx_flows_flow_pattern ON flows(flow_pattern);

-- ============================================================================
-- PACKETS TABLE (detailed packet-level data)
-- ============================================================================

CREATE TABLE IF NOT EXISTS packets (
    -- Identity
    id BIGSERIAL PRIMARY KEY,
    flow_id VARCHAR(255) NOT NULL REFERENCES flows(flow_id) ON DELETE CASCADE,
    packet_num INTEGER NOT NULL,

    -- Packet metadata
    size_bytes INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,

    -- Semantic intent (per-packet)
    intent VARCHAR(50) NOT NULL,
    layer7_protocol VARCHAR(20),

    -- LJPW coordinates (per-packet)
    love DECIMAL(3,2) NOT NULL CHECK (love >= 0 AND love <= 1),
    justice DECIMAL(3,2) NOT NULL CHECK (justice >= 0 AND justice <= 1),
    power DECIMAL(3,2) NOT NULL CHECK (power >= 0 AND power <= 1),
    wisdom DECIMAL(3,2) NOT NULL CHECK (wisdom >= 0 AND wisdom <= 1),

    -- Semantic analysis
    semantic_description TEXT,
    confidence DECIMAL(3,2) CHECK (confidence >= 0 AND confidence <= 1),

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_flow_packet UNIQUE (flow_id, packet_num)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_packets_flow_id ON packets(flow_id, packet_num);
CREATE INDEX IF NOT EXISTS idx_packets_timestamp ON packets(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_packets_intent ON packets(intent);

-- ============================================================================
-- ANALYSIS RESULTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS analysis_results (
    -- Identity
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Target
    target VARCHAR(255) NOT NULL,
    network_type VARCHAR(50),

    -- LJPW coordinates
    love DECIMAL(3,2) NOT NULL CHECK (love >= 0 AND love <= 1),
    justice DECIMAL(3,2) NOT NULL CHECK (justice >= 0 AND justice <= 1),
    power DECIMAL(3,2) NOT NULL CHECK (power >= 0 AND power <= 1),
    wisdom DECIMAL(3,2) NOT NULL CHECK (wisdom >= 0 AND wisdom <= 1),

    -- Analysis results
    health_score DECIMAL(3,2) NOT NULL CHECK (health_score >= 0 AND health_score <= 1),
    interpretation TEXT NOT NULL,
    recommendations TEXT[],

    -- Performance
    duration_ms DECIMAL(10,2),

    -- Timestamps
    analyzed_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Metadata
    api_version VARCHAR(20),
    analyzer_version VARCHAR(20)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_analysis_target ON analysis_results(target);
CREATE INDEX IF NOT EXISTS idx_analysis_analyzed_at ON analysis_results(analyzed_at DESC);
CREATE INDEX IF NOT EXISTS idx_analysis_health_score ON analysis_results(health_score);

-- ============================================================================
-- SEMANTIC MISMATCHES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS semantic_mismatches (
    -- Identity
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Reference
    flow_id VARCHAR(255) REFERENCES flows(flow_id) ON DELETE CASCADE,
    analysis_id UUID REFERENCES analysis_results(id) ON DELETE CASCADE,

    -- Mismatch details
    dimension VARCHAR(20) NOT NULL,  -- love, justice, power, wisdom
    observed DECIMAL(3,2) NOT NULL CHECK (observed >= 0 AND observed <= 1),
    expected DECIMAL(3,2) NOT NULL CHECK (expected >= 0 AND expected <= 1),
    delta DECIMAL(3,2) NOT NULL,  -- abs(observed - expected)
    severity VARCHAR(20) NOT NULL,  -- minor, moderate, major, critical

    -- Explanation
    explanation TEXT NOT NULL,
    context JSONB,  -- Additional context as JSON

    -- Timestamps
    detected_at TIMESTAMP NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMP,

    CONSTRAINT mismatch_reference CHECK (
        (flow_id IS NOT NULL) OR (analysis_id IS NOT NULL)
    )
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_mismatches_flow_id ON semantic_mismatches(flow_id);
CREATE INDEX IF NOT EXISTS idx_mismatches_analysis_id ON semantic_mismatches(analysis_id);
CREATE INDEX IF NOT EXISTS idx_mismatches_severity ON semantic_mismatches(severity);
CREATE INDEX IF NOT EXISTS idx_mismatches_detected_at ON semantic_mismatches(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_mismatches_unresolved ON semantic_mismatches(resolved_at) WHERE resolved_at IS NULL;

-- ============================================================================
-- NETWORK TARGETS TABLE (configuration)
-- ============================================================================

CREATE TABLE IF NOT EXISTS network_targets (
    -- Identity
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Target details
    name VARCHAR(255) UNIQUE NOT NULL,
    host VARCHAR(255) NOT NULL,
    description TEXT,

    -- Expected baseline
    expected_love DECIMAL(3,2) CHECK (expected_love >= 0 AND expected_love <= 1),
    expected_justice DECIMAL(3,2) CHECK (expected_justice >= 0 AND expected_justice <= 1),
    expected_power DECIMAL(3,2) CHECK (expected_power >= 0 AND expected_power <= 1),
    expected_wisdom DECIMAL(3,2) CHECK (expected_wisdom >= 0 AND expected_wisdom <= 1),

    -- Monitoring
    monitor_enabled BOOLEAN DEFAULT true,
    monitor_interval_seconds INTEGER DEFAULT 300,

    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_checked_at TIMESTAMP
);

-- Index
CREATE INDEX IF NOT EXISTS idx_targets_monitor_enabled ON network_targets(monitor_enabled) WHERE monitor_enabled = true;

-- ============================================================================
-- PATTERN MATCHES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS pattern_matches (
    -- Identity
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Reference
    flow_id VARCHAR(255) REFERENCES flows(flow_id) ON DELETE CASCADE,

    -- Pattern details
    pattern_name VARCHAR(100) NOT NULL,
    pattern_category VARCHAR(50),
    confidence DECIMAL(3,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),

    -- Match details
    matching_features TEXT[],
    explanation TEXT,

    -- Timestamps
    matched_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_pattern_matches_flow_id ON pattern_matches(flow_id);
CREATE INDEX IF NOT EXISTS idx_pattern_matches_pattern_name ON pattern_matches(pattern_name);
CREATE INDEX IF NOT EXISTS idx_pattern_matches_matched_at ON pattern_matches(matched_at DESC);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Recent suspicious flows
CREATE OR REPLACE VIEW v_recent_suspicious_flows AS
SELECT
    f.flow_id,
    f.src_ip,
    f.dst_ip,
    f.dst_port,
    f.dominant_intent,
    f.anomaly_score,
    f.anomaly_reasons,
    f.started_at,
    COUNT(sm.id) as mismatch_count
FROM flows f
LEFT JOIN semantic_mismatches sm ON f.flow_id = sm.flow_id
WHERE f.is_suspicious = true
GROUP BY f.id, f.flow_id, f.src_ip, f.dst_ip, f.dst_port, f.dominant_intent, f.anomaly_score, f.anomaly_reasons, f.started_at
ORDER BY f.started_at DESC;

-- View: LJPW health summary
CREATE OR REPLACE VIEW v_ljpw_health_summary AS
SELECT
    DATE_TRUNC('hour', analyzed_at) as hour,
    AVG(love) as avg_love,
    AVG(justice) as avg_justice,
    AVG(power) as avg_power,
    AVG(wisdom) as avg_wisdom,
    AVG(health_score) as avg_health_score,
    COUNT(*) as analysis_count
FROM analysis_results
WHERE analyzed_at > NOW() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', analyzed_at)
ORDER BY hour DESC;

-- View: Top destinations
CREATE OR REPLACE VIEW v_top_destinations AS
SELECT
    dst_ip,
    COUNT(*) as flow_count,
    AVG(love) as avg_love,
    AVG(justice) as avg_justice,
    AVG(power) as avg_power,
    AVG(wisdom) as avg_wisdom,
    SUM(CASE WHEN is_suspicious THEN 1 ELSE 0 END) as suspicious_count,
    MAX(started_at) as last_seen
FROM flows
WHERE started_at > NOW() - INTERVAL '1 hour'
GROUP BY dst_ip
ORDER BY flow_count DESC
LIMIT 20;

-- View: Intent distribution
CREATE OR REPLACE VIEW v_intent_distribution AS
SELECT
    dominant_intent,
    COUNT(*) as flow_count,
    AVG(anomaly_score) as avg_anomaly_score,
    SUM(CASE WHEN is_suspicious THEN 1 ELSE 0 END) as suspicious_count
FROM flows
WHERE started_at > NOW() - INTERVAL '1 hour'
GROUP BY dominant_intent
ORDER BY flow_count DESC;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function: Update flow ended_at on packet insert
CREATE OR REPLACE FUNCTION update_flow_ended_at()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE flows
    SET ended_at = NEW.timestamp,
        packet_count = packet_count + 1,
        byte_count = byte_count + NEW.size_bytes,
        duration_seconds = EXTRACT(EPOCH FROM (NEW.timestamp - started_at))
    WHERE flow_id = NEW.flow_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Update flow on packet insert
CREATE TRIGGER trigger_update_flow_ended_at
    AFTER INSERT ON packets
    FOR EACH ROW
    EXECUTE FUNCTION update_flow_ended_at();

-- Function: Update target last_checked_at
CREATE OR REPLACE FUNCTION update_target_last_checked()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE network_targets
    SET last_checked_at = NEW.analyzed_at
    WHERE host = NEW.target;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Update target on analysis
CREATE TRIGGER trigger_update_target_last_checked
    AFTER INSERT ON analysis_results
    FOR EACH ROW
    EXECUTE FUNCTION update_target_last_checked();

-- ============================================================================
-- SAMPLE DATA (for testing)
-- ============================================================================

-- Insert sample target
INSERT INTO network_targets (name, host, description, expected_love, expected_justice, expected_power, expected_wisdom)
VALUES (
    'Google DNS',
    '8.8.8.8',
    'Public DNS resolver - should have high Love and Wisdom',
    0.9,
    0.4,
    0.7,
    0.9
) ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- GRANTS (adjust for your users)
-- ============================================================================

-- Grant permissions to network_pinpointer user (if exists)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO network_pinpointer;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO network_pinpointer;

-- ============================================================================
-- MAINTENANCE
-- ============================================================================

-- Function: Clean old data (run periodically)
CREATE OR REPLACE FUNCTION cleanup_old_data(days_to_keep INTEGER DEFAULT 90)
RETURNS TABLE (
    flows_deleted BIGINT,
    packets_deleted BIGINT,
    analysis_deleted BIGINT,
    mismatches_deleted BIGINT
) AS $$
DECLARE
    cutoff_date TIMESTAMP;
    flows_count BIGINT;
    packets_count BIGINT;
    analysis_count BIGINT;
    mismatches_count BIGINT;
BEGIN
    cutoff_date := NOW() - (days_to_keep || ' days')::INTERVAL;

    -- Delete old packets
    WITH deleted AS (
        DELETE FROM packets
        WHERE timestamp < cutoff_date
        RETURNING 1
    )
    SELECT COUNT(*) INTO packets_count FROM deleted;

    -- Delete old flows
    WITH deleted AS (
        DELETE FROM flows
        WHERE started_at < cutoff_date
        RETURNING 1
    )
    SELECT COUNT(*) INTO flows_count FROM deleted;

    -- Delete old analysis results
    WITH deleted AS (
        DELETE FROM analysis_results
        WHERE analyzed_at < cutoff_date
        RETURNING 1
    )
    SELECT COUNT(*) INTO analysis_count FROM deleted;

    -- Delete old resolved mismatches
    WITH deleted AS (
        DELETE FROM semantic_mismatches
        WHERE resolved_at IS NOT NULL AND resolved_at < cutoff_date
        RETURNING 1
    )
    SELECT COUNT(*) INTO mismatches_count FROM deleted;

    RETURN QUERY SELECT flows_count, packets_count, analysis_count, mismatches_count;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- COMPLETED
-- ============================================================================

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Network Pinpointer database schema initialized successfully!';
    RAISE NOTICE 'Tables created: flows, packets, analysis_results, semantic_mismatches, network_targets, pattern_matches';
    RAISE NOTICE 'Views created: v_recent_suspicious_flows, v_ljpw_health_summary, v_top_destinations, v_intent_distribution';
    RAISE NOTICE 'Ready for LJPW semantic analysis!';
END $$;

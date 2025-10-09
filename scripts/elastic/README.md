Here’s a clean, developer-friendly **README.md** explaining your setup and the `es-manage` backup/restore flow.

---

# 🗂️ Elasticsearch Snapshot Management

This repository includes helper scripts and Docker Compose configuration to easily **back up**, **restore**, and **move** your Elasticsearch data across environments.

It’s designed for the single-node setup defined in `docker-compose.yml`, using:

* **Elasticsearch 8.x**
* **Kibana**
* Optional supporting containers (`n8n`, `RabbitMQ`, etc.)

---

## ⚙️ How It Works

Elasticsearch supports **snapshots**—point-in-time backups of indices and cluster state.
Your Docker Compose file mounts a snapshot directory:

```yaml
volumes:
  - ./es_snapshots:/usr/share/elasticsearch/snapshots
```

and declares a `path.repo`:

```yaml
environment:
  - path.repo=/usr/share/elasticsearch/snapshots
```

This allows Elasticsearch to write backups into that folder.
From there, you can:

* **Trigger snapshots** using the REST API (wrapped by the scripts)
* **Restore** data into the same or a new cluster
* **Archive** snapshot folders (`.tgz`) for transfer

---

## 🧰 Scripts Overview

Both scripts support the same commands:

| Command                              | Description                                                           |
| ------------------------------------ | --------------------------------------------------------------------- |
| `register`                           | Register the snapshot repository (`local_fs`) inside Elasticsearch    |
| `backup`                             | Create a new timestamped snapshot                                     |
| `list`                               | Show all existing snapshots                                           |
| `restore <SNAPSHOT>`                 | Restore a snapshot (includes global state)                            |
| `restore-prefix <SNAPSHOT> [PREFIX]` | Restore snapshot into new indices with a prefix (default `restored_`) |
| `archive`                            | Compress the `./es_snapshots` folder into a `.tgz` archive            |

### Environment Variables

| Variable                       | Default          | Purpose                                      |
| ------------------------------ | ---------------- | -------------------------------------------- |
| `HOST_PORT_ELASTICSEARCH_HTTP` | `9200`           | Port exposed by your Elasticsearch container |
| `SNAP_REPO`                    | `local_fs`       | Repository name for snapshots                |
| `SNAP_DIR`                     | `./es_snapshots` | Local snapshot directory mounted in Docker   |

---

## 🚀 Quick Start

### 1. Register the repository

Run once after first start-up:

```bash
./es-manage.sh register
# or
es-manage.bat register
```

### 2. Create a snapshot

```bash
./es-manage.sh backup
```

Output example:

```
Creating snapshot snap-20251008-162345 ...
Done. Snapshot name: snap-20251008-162345
```

### 3. List snapshots

```bash
./es-manage.sh list
```

### 4. Restore a snapshot

Stops writes to Elasticsearch first (recommended).

#### a) Replace all indices

```bash
./es-manage.sh restore snap-20251008-162345
```

#### b) Restore into prefixed indices

```bash
./es-manage.sh restore-prefix snap-20251008-162345 myprefix_
```

### 5. Archive snapshots

To move to another host or repo:

```bash
./es-manage.sh archive
# creates es_snapshots_20251008_162345.tgz
```

Copy that archive to another instance, extract it into `./es_snapshots`,
and re-register the repo (`register` command).

---

## 💾 Moving Between Environments

1. Stop your writer apps to freeze state (if possible).
2. Run `./es-manage.sh backup`.
3. `tar` the `./es_snapshots` folder (or use `archive`).
4. On the new host:

   * Copy your `es_snapshots` folder.
   * Use the same `docker-compose.yml`.
   * Run `./es-manage.sh register`.
   * Run `./es-manage.sh restore <snapshot_name>`.

---

## ⚠️ Notes and Best Practices

* Snapshots are **incremental** — new snapshots reuse unchanged data.
* The **same Elasticsearch version** must be used for restore.
* Keep `path.repo` consistent (`/usr/share/elasticsearch/snapshots`).
* The snapshot directory must be **mounted** and **writable** by the ES container.
* You can automate periodic backups with a cron job (e.g., daily `backup` + `archive`).

---

## 🧩 Integration with Docker Compose

Elasticsearch and Kibana compose services are already configured:

```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.15.2
  ports:
    - "9200:9200"
  environment:
    - discovery.type=single-node
    - xpack.security.enabled=false
    - ES_JAVA_OPTS=-Xms1g -Xmx1g
    - path.repo=/usr/share/elasticsearch/snapshots
  volumes:
    - es_data:/usr/share/elasticsearch/data
    - ./es_snapshots:/usr/share/elasticsearch/snapshots
```

---

## 🧹 Clean-up Commands

Remove old snapshots:

```bash
curl -X DELETE "http://localhost:9200/_snapshot/local_fs/snap-20251001-120000"
```

Delete all local snapshot files:

```bash
rm -rf ./es_snapshots/*
```

---

## ✅ Summary

| Task                | Command                                         |
| ------------------- | ----------------------------------------------- |
| Register repo       | `./es-manage.sh register`                       |
| Backup data         | `./es-manage.sh backup`                         |
| List backups        | `./es-manage.sh list`                           |
| Restore snapshot    | `./es-manage.sh restore <name>`                 |
| Restore with prefix | `./es-manage.sh restore-prefix <name> <prefix>` |
| Archive snapshots   | `./es-manage.sh archive`                        |

---

Would you like me to include a **Windows PowerShell** version too (for environments without `curl.exe` or `tar.exe`)? It can provide nicer progress bars and JSON parsing.

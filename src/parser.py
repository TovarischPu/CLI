import xml.etree.ElementTree as ET

MAVEN_NS = "http://maven.apache.org/POM/4.0.0"


def build_pom_url(source: str, package: str) -> str:
    group, artifact, version = package.split(":")
    group_path = group.replace(".", "/")
    return (
        f"{source.rstrip('/')}/{group_path}/{artifact}/"
        f"{version}/{artifact}-{version}.pom"
    )


def parse_direct_dependencies(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    dependencies = []
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"
    deps_container = root.find(f"{ns}dependencies")
    if deps_container is None:
        return dependencies
    for dep in deps_container.findall(f"{ns}dependency"):
        group = dep.find(f"{ns}groupId")
        artifact = dep.find(f"{ns}artifactId")
        if group is not None and artifact is not None:
            dependencies.append({
                "groupId": group.text,
                "artifactId": artifact.text,
            })
    return dependencies
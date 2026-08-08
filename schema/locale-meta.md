# Locale pack meta schema

## L1 `_meta.yaml`

```yaml
level: 1
country: in
name: India
admin_labels:
  l2: state          # or province, governorate, region...
  l3: district       # or county, municipality, LGA...
languages_default: [hi, en]
currency: INR
status: seeded       # listed | seeded | verified
maintainers: []
```

## L2 `_meta.yaml`

```yaml
level: 2
country: in
l2: uttar-pradesh
name: Uttar Pradesh
languages: [hi, ur, en]
status: seeded
maintainers: []
```

## L3 pack

L3 uses README frontmatter:

```yaml
level: 3
country: in
l2: uttar-pradesh
l3: varanasi
languages: [hi, bho]
status: seeded
maintainers: []
```

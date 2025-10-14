#!/usr/bin/env python3
"""
Comprehensive refactoring automation script.
This script reads Spanish files and creates English equivalents with proper translations.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Base directory
BASE_DIR = Path('/home/valerubio_7/Dev/facultad/project-SysAcad')

# Import mappings from refactoring_mappings.py
TRANSLATIONS = {
    # Classes
    'Alumno': 'Student',
    'Universidad': 'University',
    'Facultad': 'Faculty',
    'Departamento': 'Department',
    'Especialidad': 'Specialty',
    'Materia': 'Subject',
    'Cargo': 'Position',
    'Autoridad': 'Authority',
    'TipoDocumento': 'DocumentType',
    'TipoEspecialidad': 'SpecialtyType',
    'TipoDedicacion': 'DedicationType',
    'CategoriaCargo': 'PositionCategory',
    'Grado': 'Degree',
    'Grupo': 'Group',
    'Orientacion': 'Orientation',
    'Plan': 'Plan',
    'Area': 'Area',
    
    # Service/Repository/Serializer suffixes
    'Service': 'Service',
    'Repository': 'Repository',
    'Repositorio': 'Repository',
    'Serializer': 'Serializer',
    'ViewSet': 'ViewSet',
    
    # Model fields - needs word boundary matching
    r'\bnombre\b': 'name',
    r'\bapellido\b': 'last_name',
    r'\bnrodocumento\b': 'document_number',
    r'\btipo_documento\b': 'document_type',
    r'\bfecha_nacimiento\b': 'birth_date',
    r'\bsexo\b': 'gender',
    r'\bnro_legajo\b': 'student_id_number',
    r'\bfecha_ingreso\b': 'enrollment_date',
    r'\bespecialidad\b': 'specialty',
    r'\bespecialidades\b': 'specialties',
    r'\bsigla\b': 'acronym',
    r'\babreviatura\b': 'abbreviation',
    r'\bdirectorio\b': 'directory',
    r'\bcodigopostal\b': 'postal_code',
    r'\bciudad\b': 'city',
    r'\bdomicilio\b': 'address',
    r'\btelefono\b': 'phone',
    r'\bcontacto\b': 'contact_name',
    r'\buniversidad\b': 'university',
    r'\bfacultad\b': 'faculty',
    r'\bfacultades\b': 'faculties',
    r'\bletra\b': 'letter',
    r'\bobservacion\b': 'observation',
    r'\btipoespecialidad\b': 'specialty_type',
    r'\bnivel\b': 'level',
    r'\bpuntos\b': 'points',
    r'\bcategoria_cargo\b': 'position_category',
    r'\btipo_dedicacion\b': 'dedication_type',
    r'\bcargo\b': 'position',
    r'\bcargos\b': 'positions',
    r'\bmaterias\b': 'subjects',
    r'\bautoridades\b': 'authorities',
    r'\bmateria\b': 'subject',
    r'\bcodigo\b': 'code',
    r'\bfecha_inicio\b': 'start_date',
    r'\bfecha_fin\b': 'end_date',
    r'\borientaciones\b': 'orientations',
    r'\bdescripcion\b': 'description',
    r'\bplan\b': 'plan',
    r'\blibreta_civica\b': 'civic_card',
    r'\blibreta_enrolamiento\b': 'enrollment_card',
    r'\bpasaporte\b': 'passport',
    r'\balumnos\b': 'students',
    r'\bdepartamentos\b': 'departments',
    r'\bgrados\b': 'degrees',
    r'\bgrupos\b': 'groups',
    
    # Properties
    r'\bnombre_completo\b': 'full_name',
    r'\bedad\b': 'age',
    r'\bvigente\b': 'is_active',
    
    # Methods
    r'\bcrear\b': 'create',
    r'\bbuscar_por_id\b': 'find_by_id',
    r'\bbuscar_todos\b': 'find_all',
    r'\bactualizar\b': 'update',
    r'\bborrar_por_id\b': 'delete_by_id',
    r'\bencontrar_id\b': 'find_by_id',
    r'\bbuscar_por_legajo\b': 'find_by_student_id_number',
    r'\bbuscar_por_documento\b': 'find_by_document_number',
    r'\bbuscar_por_sigla\b': 'find_by_acronym',
    r'\bbuscar_con_relaciones\b': 'find_with_relations',
    r'\basociar_materia\b': 'associate_subject',
    r'\bdesasociar_materia\b': 'disassociate_subject',
    r'\basociar_facultad\b': 'associate_faculty',
    r'\bdesasociar_facultad\b': 'disassociate_faculty',
    
    # Variables
    r'\balumno_existente\b': 'existing_student',
    r'\balumno_actualizado\b': 'updated_student',
    r'\balumno\b': 'student',
    r'\btipo_doc\b': 'doc_type',
    r'\bhoy\b': 'today',
    r'\bfecha_actual\b': 'current_date',
    r'\bfecha_str\b': 'date_str',
    
    # Test helpers
    r'\bnuevoalumno\b': 'new_student',
    r'\bnuevauniversidad\b': 'new_university',
    r'\bnuevafacultad\b': 'new_faculty',
    r'\bnuevodepartamento\b': 'new_department',
    r'\bnuevaespecialidad\b': 'new_specialty',
    r'\bnuevamateria\b': 'new_subject',
    r'\bnuevocargo\b': 'new_position',
    r'\bnuevaautoridad\b': 'new_authority',
    r'\bnuevotipodocumento\b': 'new_document_type',
    r'\bnuevotipoespecialidad\b': 'new_specialty_type',
    r'\bnuevotipodedicacion\b': 'new_dedication_type',
    r'\bnuevacategoriacargo\b': 'new_position_category',
    r'\bnuevogrado\b': 'new_degree',
    r'\bnuevogrupo\b': 'new_group',
    r'\bnuevaorientacion\b': 'new_orientation',
    r'\bnuevoplan\b': 'new_plan',
    r'\bnuevaarea\b': 'new_area',
}

# File name mappings
FILE_MAPPINGS = {
    'alumno': 'student',
    'universidad': 'university',
    'facultad': 'faculty',
    'departamento': 'department',
    'especialidad': 'specialty',
    'materia': 'subject',
    'cargo': 'position',
    'autoridad': 'authority',
    'tipodocumento': 'document_type',
    'tipoespecialidad': 'specialty_type',
    'tipodedicacion': 'dedication_type',
    'categoriacargo': 'position_category',
    'grado': 'degree',
    'grupo': 'group',
    'orientacion': 'orientation',
    'plan': 'plan',
    'area': 'area',
}

def translate_content(content: str) -> str:
    """
    Translate Spanish identifiers to English in file content.
    """
    result = content
    
    # Apply translations with word boundaries
    for spanish, english in TRANSLATIONS.items():
        if spanish.startswith(r'\b'):
            # Regex pattern
            result = re.sub(spanish, english, result)
        else:
            # Simple string replacement for class names
            result = result.replace(spanish, english)
    
    return result

def translate_import_path(import_line: str) -> str:
    """
    Translate import paths from Spanish to English.
    """
    result = import_line
    
    # Translate file names in imports
    for spanish, english in FILE_MAPPINGS.items():
        result = result.replace(f'.{spanish}', f'.{english}')
        result = result.replace(f'_{spanish}_', f'_{english}_')
        result = result.replace(f'{spanish}_', f'{english}_')
    
    return result

def process_file(input_path: Path, output_path: Path) -> bool:
    """
    Process a single file: read, translate, and write to new location.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Translate content
        translated = translate_content(content)
        
        # Translate imports
        lines = translated.split('\n')
        translated_lines = []
        for line in lines:
            if 'import' in line or 'from' in line:
                translated_lines.append(translate_import_path(line))
            else:
                translated_lines.append(line)
        
        translated = '\n'.join(translated_lines)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write translated content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        print(f"✓ Created: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return False

def get_output_filename(input_filename: str) -> str:
    """
    Convert Spanish filename to English filename.
    """
    name = input_filename
    
    # Remove extension
    name_parts = name.rsplit('.', 1)
    base_name = name_parts[0]
    extension = name_parts[1] if len(name_parts) > 1 else ''
    
    # Translate parts
    for spanish, english in FILE_MAPPINGS.items():
        base_name = base_name.replace(spanish, english)
    
    # Reconstruct
    return f"{base_name}.{extension}" if extension else base_name

def process_directory(dir_name: str, input_suffix: str = '', output_suffix: str = ''):
    """
    Process all Python files in a directory.
    """
    input_dir = BASE_DIR / 'app' / dir_name
    
    if not input_dir.exists():
        print(f"Directory not found: {input_dir}")
        return
    
    print(f"\n{'='*80}")
    print(f"Processing {dir_name}...")
    print(f"{'='*80}")
    
    processed = 0
    for file_path in input_dir.glob('*.py'):
        if file_path.name == '__init__.py' or file_path.name.startswith('_'):
            continue
        
        output_filename = get_output_filename(file_path.name)
        output_path = input_dir / output_filename
        
        if output_path.exists() and not output_path.name.endswith('.old'):
            print(f"⊘ Skipping (already exists): {output_path}")
            continue
        
        if process_file(file_path, output_path):
            processed += 1
    
    print(f"\nProcessed {processed} files in {dir_name}")

def main():
    """
    Main refactoring process.
    """
    print("="*80)
    print("Django SysAcad Refactoring Automation")
    print("="*80)
    print("\nThis script will create English versions of Spanish files.")
    print("Original files will be preserved.")
    print("\nPress Ctrl+C to cancel, Enter to continue...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        return
    
    # Process each directory
    # process_directory('models')  # Already done manually
    process_directory('repositories')
    process_directory('serializers')
    process_directory('services')
    process_directory('views')
    
    # Process tests
    test_dir = BASE_DIR / 'tests'
    if test_dir.exists():
        print(f"\n{'='*80}")
        print("Processing tests...")
        print(f"{'='*80}")
        for file_path in test_dir.glob('test_*.py'):
            output_filename = get_output_filename(file_path.name)
            output_path = test_dir / output_filename
            
            if output_path.exists():
                print(f"⊘ Skipping (already exists): {output_path}")
                continue
            
            process_file(file_path, output_path)
    
    print("\n" + "="*80)
    print("Refactoring Complete!")
    print("="*80)
    print("\nNext steps:")
    print("1. Review the generated files")
    print("2. Update __init__.py files in each directory")
    print("3. Update app/urls.py")
    print("4. Run tests: python manage.py test")
    print("5. Delete old Spanish files once everything works")

if __name__ == '__main__':
    main()

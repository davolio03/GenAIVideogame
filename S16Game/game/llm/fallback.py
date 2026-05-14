# Datos de reserva — usados cuando la API LLM no esta disponible.
# Refleja la misma estructura JSON que se espera que devuelva el LLM.
# Todas las etiquetas <red> ya estan en formato {color} de Ren'Py.

def get_fallback_data(victim_name):
    """Devuelve un diccionario completo de datos de reserva cuando el LLM no esta disponible."""
    return {
        "opening_narrative": (
            "Es tarde en la noche. La lluvia cae a cantaros.\n\n"
            "Un telefono suena de forma estridente, rompiendo el silencio de la oficina.\n\n"
            "El reconocido magnate Don Alejandro Montemayor ha sido hallado muerto en la biblioteca de su propia mansion.\n\n"
            "Como el detective mas celebre de la ciudad, te convocan a la escena de inmediato.\n\n"
            "Ocho personas estaban en la mansion esa noche — pero ahora, solo quedan siete.\n\n"
            "{} esta muerto. Asesinado.\n\n"
            "Debes descubrir la verdad."
        ).format(victim_name),

        "locations": {
            "salon": {
                "description": (
                    "Salon — Amplio y majestuoso, una enorme arana de cristal cuelga del centro del techo.\n\n"
                    "El suelo de marmol brilla como un espejo, reflejando el tenue resplandor de la arana.\n\n"
                    "Junto a la escalera de caracol que sube al piso superior, una {color=#ff4444}marca oscura y rojiza{/color} ha sido limpiada apresuradamente.\n\n"
                    "[npc_here_name] esta de pie cerca de la chimenea, con los brazos cruzados, observandote fijamente."
                ),
                "clue": (
                    "Recorres el salon lentamente, examinando cada rincon con atencion.\n\n"
                    "El pasamanos de la escalera no tiene huellas dactilares. Una {color=#ff4444}pequena marca de quemadura{/color} afea el borde de la alfombra.\n\n"
                    "En el retrato familiar sobre la chimenea, los ojos de Don Alejandro Montemayor parecen delatar una profunda inquietud."
                ),
            },
            "master_bedroom": {
                "description": (
                    "Dormitorio Principal — Cortinas de terciopelo carmesi oscuro bloquean la mayoria de las ventanas.\n\n"
                    "Un leve aroma a perfume flota en el aire.\n\n"
                    "Sobre la mesilla de noche reposa una copa de vino tinto a medio terminar y un libro abierto.\n\n"
                    "[npc_here_name] esta aqui, mirando nerviosamente hacia la puerta."
                ),
                "clue": (
                    "Examinas el dormitorio principal. Filas de decoracion costosa se alinean en perfecto orden sobre los estantes.\n\n"
                    "Dentro del cajon del armario, encuentras {color=#ff4444}una carta con caligrafia erraticaa{/color} — parece una amenaza.\n\n"
                    "Una leve marca de arrastre cruza el suelo, desde la entrada hasta la ventana."
                ),
            },
            "guest_quarters": {
                "description": (
                    "Habitacion de Invitados — Sencilla y ordenada, como si rara vez se usara.\n\n"
                    "La cama esta hecha con precision de hotel. La lampara de noche sigue encendida.\n\n"
                    "Una maleta de viaje cubierta de etiquetas de equipaje de todo el mundo descansa sobre el alfeizar.\n\n"
                    "[npc_here_name] permanece junto a la ventana, recortado contra la lluvia."
                ),
                "clue": (
                    "Abres la maleta. Nada dentro salvo ropa corriente y articulos de aseo.\n\n"
                    "Bajo la almohada hay un diario, pero {color=#ff4444}la mayoria de sus paginas han sido arrancadas{/color}.\n\n"
                    "En la papelera, un papel arrugado muestra un unico numero de telefono borroso."
                ),
            },
            "kitchen": {
                "description": (
                    "Cocina — Una amplia cocina moderna equipada con electrodomesticos de ultima generacion.\n\n"
                    "Una olla de la cena de anoche sigue sobre la estufa, su contenido ya coagulado.\n\n"
                    "Hay un {color=#ff4444}leve y amargo olor a almendras{/color} en el aire.\n\n"
                    "[npc_here_name] se apoya en la encimera, mirando la olla coagulada."
                ),
                "clue": (
                    "Revisas el frigorifico y la despensa. Todo esta meticulosamente organizado.\n\n"
                    "En el cubo de basura, {color=#ff4444}una copa de vino rota con residuo rojo seco{/color}.\n\n"
                    "Bajo el fregadero, una botella de vidrio marron sin etiqueta esta oculta tras los productos de limpieza."
                ),
            },
            "garden": {
                "description": (
                    "Jardin — Setos cuidadosamente recortados proyectan sombras inquietantes bajo la luz de la luna.\n\n"
                    "Las rosas estan en plena floracion, pero {color=#ff4444}un parche de tierra cerca del muro lejano parece recien removido{/color}.\n\n"
                    "A lo lejos, un buho ulula en la noche.\n\n"
                    "[npc_here_name] pasea lentamente por el sendero de setos, sumido en sus pensamientos."
                ),
                "clue": (
                    "Te acercas a la tierra removida. Una caja metalica ha sido enterrada aqui.\n\n"
                    "La caja esta vacia, pero {color=#ff4444}manchas de sangre seca cubren su interior{/color}.\n\n"
                    "Entre los macizos de flores, descubres una huella parcial — aproximadamente una talla 44."
                ),
            },
            "pool": {
                "description": (
                    "Piscina — El agua esta perfectamente quieta, un espejo que refleja las estrellas dispersas en el cielo.\n\n"
                    "Una toalla humeda esta colocada sobre una de las tumbonas.\n\n"
                    "La puerta del vestuario en la esquina permanece entreabierta.\n\n"
                    "[npc_here_name] esta sentado en una de las tumbonas, mirando fijamente la superficie del agua."
                ),
                "clue": (
                    "Rodeas la piscina, buscando cualquier cosa fuera de lugar.\n\n"
                    "Dentro del vestuario, {color=#ff4444}una camisa empapada con una nota danada por el agua{/color} en su bolsillo.\n\n"
                    "Huellas embarradas salpican las baldosas cerca del borde de la piscina — alguien paso por aqui desde el jardin."
                ),
            },
            "library": {
                "description": (
                    "Biblioteca — El santuario privado de Don Alejandro Montemayor. Estanterias cubren cada pared del suelo al techo.\n\n"
                    "Un escritorio de caoba esta cubierto de documentos y libros de contabilidad.\n\n"
                    "En el suelo, un {color=#ff4444}contorno de tiza marca donde cayo el cuerpo{/color}.\n\n"
                    "Este — es el escenario del crimen.\n\n"
                    "[npc_here_name] esta de pie en un extremo de la habitacion, sin poder apartar la mirada del contorno de tiza en el suelo."
                ),
                "clue": (
                    "Examinas el escritorio detenidamente. {color=#ff4444}La ultima pagina de un cuaderno ha sido arrancada{/color}.\n\n"
                    "Una caja fuerte de pared cuelga abierta, sin contener mas que una pila de carpetas vacias.\n\n"
                    "Mientras inspeccionas la estanteria, notas algo extrano en un ejemplar de 'El Sabueso de los Baskerville'.\n\n"
                    "Alargas la mano hacia el. El libro no se mueve. Empujas con mas fuerza —\n\n"
                    "Clic. ¡Toda la estanteria se abre girando, revelando una habitacion oculta!"
                ),
            },
            "hidden_room": {
                "description": (
                    "Habitacion Oculta — Estrecha y sombria, iluminada solo por una unica bombilla parpadeante.\n\n"
                    "Las paredes estan cubiertas de fotografias y recortes de periodico, conectados por {color=#ff4444}una red de hilo rojo{/color}.\n\n"
                    "En la esquina hay un viejo armario metalico, cubierto de polvo."
                ),
                "clue": (
                    "Estudias la red de pistas en la pared.\n\n"
                    "Las fotografias incluyen a Don Alejandro Montemayor, sus socios comerciales, su familia — y rostros que no reconoces.\n\n"
                    "El armario metalico contiene {color=#ff4444}un fajo de cartas y un contrato sin firmar{/color}.\n\n"
                    "Esta habitacion guarda demasiados secretos para contarlos..."
                ),
            },
        },

        "npcs": {
            "elias": {
                "mood": "nervioso, evita el contacto visual directo",
                "dialogues": [
                    {"question": "Donde estaba usted la noche del crimen?",
                     "answer": "Estaba en la {color=#ff4444}cocina preparando el te de la noche{/color}. La rutina de esta casa no se detiene por nadie."},
                    {"question": "Noto algo extrano ultimamente?",
                     "answer": "El señor habia estado recibiendo cartas amenazantes. {color=#ff4444}Quemo la mayoria de ellas{/color} en la chimenea."},
                    {"question": "Como era su relacion con la victima?",
                     "answer": "Le servi fielmente durante veinte años. Era... un hombre complicado. Generoso con unos, despiadado con otros."},
                    {"question": "Quien cree que pudo haberlo hecho?",
                     "answer": "Tengo mis sospechas, detective. Pero no me corresponde acusar. Fijese bien en los invitados."},
                ],
            },
            "caterina": {
                "mood": "visiblemente afectada, pero su compostura parece forzada",
                "dialogues": [
                    {"question": "Cuando vio a su esposo con vida por ultima vez?",
                     "answer": "En la cena. Parecia {color=#ff4444}preocupado, apenas probo la comida{/color}. Luego se fue a la biblioteca."},
                    {"question": "Tenia su esposo problemas con alguien?",
                     "answer": "Alejandro Montemayor tenia rivales en todas partes. Negocios, politica... incluso dentro de estas paredes."},
                    {"question": "Quien se beneficia de su muerte?",
                     "answer": "La herencia es... sustancial. {color=#ff4444}Pero daria hasta el ultimo centavo{/color} por tenerlo de vuelta."},
                    {"question": "Sabe algo sobre la habitacion oculta tras la estanteria?",
                     "answer": "¿Habitacion oculta? Yo... no. Mi esposo me ocultaba muchas cosas, detective."},
                ],
            },
            "isabella": {
                "mood": "con lagrimas en los ojos, pero se vuelve intensa al responder",
                "dialogues": [
                    {"question": "Era cercana a su padre?",
                     "answer": "Lo eramos. Pero ultimamente habia estado {color=#ff4444}distante, mirando por encima del hombro{/color} constantemente."},
                    {"question": "Tenia su padre enemigos?",
                     "answer": "Era un hombre poderoso. El poder atrae enemigos como la miel atrae a las moscas."},
                    {"question": "Donde estaba usted cuando ocurrio?",
                     "answer": "Estaba en el jardin. Me gusta caminar entre las rosas cuando no puedo dormir."},
                    {"question": "Que sabe de los otros invitados?",
                     "answer": "Todos aqui tienen secretos. Incluso yo, detective. Pero ninguno por el que valga la pena matar."},
                ],
            },
            "blanco": {
                "mood": "tranquilo y calculador, midiendo cada palabra",
                "dialogues": [
                    {"question": "Que le trae a la mansion?",
                     "answer": "Alejandro Montemayor y yo teniamos... {color=#ff4444}asuntos que discutir. Asuntos pendientes{/color}."},
                    {"question": "Donde estaba usted a la hora del crimen?",
                     "answer": "Estaba en la habitacion de invitados, revisando unos documentos. {color=#ff4444}Solo, por desgracia{/color}."},
                    {"question": "Conocia bien a la victima?",
                     "answer": "Fuimos socios una vez. Luego rivales. Luego algo intermedio. Es... complicado."},
                    {"question": "Hay algo que no me este contando?",
                     "answer": "Detective, todos en esta casa esconden algo. La pregunta es — ¿el secreto de quien valia la pena matar?"},
                ],
            },
            "fernando": {
                "mood": "pulido y diplomatico, casi ensayado",
                "dialogues": [
                    {"question": "Donde estaba usted la noche del crimen?",
                     "answer": "Estaba en mi habitacion, leyendo. {color=#ff4444}El Conde de Montecristo{/color}. Muy apropiado, dadas las circunstancias."},
                    {"question": "Cual era su relacion con Alejandro Montemayor?",
                     "answer": "Nos moviamos en los mismos circulos. Lo respetaba como empresario — no necesariamente como hombre."},
                    {"question": "Noto algo inusual esta noche?",
                     "answer": "El mayordomo no era el mismo durante la cena. {color=#ff4444}Nervioso. Dejo caer una bandeja de copas{/color}."},
                    {"question": "Que opina de los otros invitados?",
                     "answer": "Digamos simplemente que he visto mejor compañia en un funeral. Y peor."},
                ],
            },
            "elena": {
                "mood": "callada y observadora, responde con cuidado preciso",
                "dialogues": [
                    {"question": "Como conocia a Alejandro Montemayor?",
                     "answer": "Nos conocimos por negocios. Fui su {color=#ff4444}consultora de arte durante muchos años{/color}."},
                    {"question": "Donde estaba cuando ocurrio?",
                     "answer": "Estaba en el salon, junto a la ventana. Mirando la lluvia. Esperando."},
                    {"question": "Esperando que?",
                     "answer": "Esperando que algo terminara. {color=#ff4444}No esperaba que terminara asi{/color}."},
                    {"question": "Vio a alguien pasar por el salon?",
                     "answer": "Vi una figura dirigirse hacia la biblioteca. Pero la arana estaba tenue — no pude distinguir quien era."},
                ],
            },
            "isolda": {
                "mood": "impaciente y autoritaria, claramente acostumbrada a estar al mando",
                "dialogues": [
                    {"question": "Cual era su relacion con el difunto?",
                     "answer": "Alejandro Montemayor y yo eramos {color=#ff4444}viejos amigos. Lo conoci antes del dinero{/color}, antes de la mansion."},
                    {"question": "Cree que alguien en esta casa lo mato?",
                     "answer": "Por supuesto. El asesinato casi siempre es personal. Y casi siempre viene de dentro."},
                    {"question": "Donde estaba usted durante el crimen?",
                     "answer": "Estaba en el dormitorio principal, descansando. A mi edad, una necesita descansar con frecuencia."},
                    {"question": "Hay algo mas que deba saber?",
                     "answer": "El jardinero no vino hoy. {color=#ff4444}Primera vez en diez años{/color}. Saque usted sus propias conclusiones."},
                ],
            },
            "will": {
                "mood": "inquieto, mirando constantemente por encima del hombro",
                "dialogues": [
                    {"question": "Que fue lo que oyo anoche?",
                     "answer": "Una discusion. {color=#ff4444}Voces elevadas que venian de la biblioteca{/color}. Luego silencio. Un silencio terrible."},
                    {"question": "Reconocio las voces?",
                     "answer": "Una era sin duda Alejandro Montemayor. La otra... no estoy seguro. Estaba amortiguada."},
                    {"question": "Cual es su papel en esta casa?",
                     "answer": "Soy amigo de la familia. O lo era. Vine a pasar la semana y acabe en la escena de un crimen."},
                    {"question": "Sospecha de alguien?",
                     "answer": "No quiero señalar a nadie. Pero {color=#ff4444}el dolor de la viuda parece... ensayado{/color}."},
                ],
            },
        },

        "weapons": {
            "Pistol": {"inspect_text": "Una pistola semiautomatica elegante. El {color=#ff4444}numero de serie ha sido limado{/color}. Un leve olor a polvora aun impregna el cañon."},
            "Trophy": {"inspect_text": "Un pesado trofeo dorado, deslucido por el paso del tiempo. La base esta {color=#ff4444}abollada — como si hubiera sido usado para golpear algo{/color}. O a alguien."},
            "Flowerpot": {"inspect_text": "Una gran maceta de terracota. La tierra sigue humeda. Hay {color=#ff4444}marcas de aranazos recientes en el borde{/color}."},
            "Shears": {"inspect_text": "Un par de tijeras de jardineria pesadas. Las hojas estan {color=#ff4444}afiladas y limpias — quizas demasiado limpias{/color}. Ni una mota de oxido."},
            "Hose": {"inspect_text": "Una manguera de goma gruesa, sorprendentemente pesada. {color=#ff4444}Marcas de lazo en la superficie{/color} sugieren que fue atada en un nudo recientemente."},
            "Pillow": {"inspect_text": "Una almohada de plumas mullida. La tela esta {color=#ff4444}arrugada en el centro{/color}, como si hubiera sido presionada con gran fuerza."},
            "Knife": {"inspect_text": "Un cuchillo de chef del bloque de cocina. La hoja esta impecable, pero una {color=#ff4444}tenue marca rojiza persiste donde el mango se une al acero{/color}."},
            "Letter Opener": {"inspect_text": "Un abrecartas de plata ornamentado. Elegante pero terriblemente afilado. Un monograma en el mango dice {color=#ff4444}'A.M.'{/color}."},
            "Candelabra": {"inspect_text": "Un pesado candelabro de bronce. {color=#ff4444}Un brazo esta doblado en un angulo extrano{/color}. Cera seca gotea por el costado como lagrimas congeladas."},
            "Baseball Bat": {"inspect_text": "Un bate de beisbol de madera desgastado. La cinta de agarre se esta despegando. Hay {color=#ff4444}marcas de rozaduras cerca del extremo del barril{/color}."},
            "Brass Knuckles": {"inspect_text": "Un juego de punos americanos, frios y solidos. El metal esta {color=#ff4444}rayado — evidencia de uso previo{/color}."},
            "Poison": {"inspect_text": "Un pequeno frasco de vidrio sin etiqueta. El liquido en su interior es {color=#ff4444}transparente e inodoro{/color}. Una sola gota podria ser letal."},
            "Hammer": {"inspect_text": "Un martillo de carpintero estandar. La cabeza esta limpia, pero el {color=#ff4444}mango tiene leves marcas oscuras{/color}."},
        },

        "accusation_outcomes": {
            "correct": (
                "Unes las piezas de la evidencia. Las contradicciones. Las pistas resaltadas en rojo.\n\n"
                "Reunes a todos en el salon. Tus deducciones trazan una cadena irrefutable de acontecimientos.\n\n"
                "El asesino — confrontado con la verdad — finalmente se derrumba.\n\n"
                "\"Si. Lo hice.\" La confesion resuena por toda la mansion silenciosa.\n\n"
                "Se hace justicia. El caso esta cerrado."
            ),
            "wrong_murderer": (
                "Presentas tu acusacion con confianza.\n\n"
                "Pero la persona que has nombrado da un paso al frente con una coartada solida — corroborada por otros dos testigos.\n\n"
                "La sala queda en silencio. Sientes cada par de ojos sobre ti.\n\n"
                "Vuelta a la investigacion. El verdadero asesino sigue en esta casa."
            ),
            "wrong_weapon": (
                "Levantas la supuesta arma del crimen.\n\n"
                "El forense niega con la cabeza. \"El patron de la herida no coincide. Ni de lejos.\"\n\n"
                "Un murmullo recorre la sala. Tu teoria se desmorona.\n\n"
                "Debes reconsiderar las pruebas."
            ),
            "wrong_location": (
                "Declaras la escena del crimen con autoridad.\n\n"
                "Pero algo no cuadra. Las pruebas fisicas no coinciden con tu teoria.\n\n"
                "\"Detective, ¿esta seguro?\" Alguien pregunta. La duda en su voz es inconfundible.\n\n"
                "Te equivocaste sobre donde ocurrio. ¿En que mas te habras equivocado?"
            ),
            "wrong_accomplice": (
                "Señalas al supuesto complice.\n\n"
                "El acusado parece genuinamente desconcertado — y varios testigos confirman su paradero.\n\n"
                "Puede que aun haya una conspiracion... pero esta persona no forma parte de ella.\n\n"
                "La investigacion debe continuar."
            ),
            "all_wrong": (
                "Tu acusacion se desmorona casi de inmediato.\n\n"
                "Cada elemento — sospechoso, arma, lugar, complice — es contradicho por las pruebas.\n\n"
                "Los invitados intercambian miradas inquietas. Su confianza en ti se ha evaporado.\n\n"
                "Has fallado. El asesino queda libre, y el oscuro secreto de la mansion permanece enterrado."
            ),
        },
    }

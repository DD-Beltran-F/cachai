# Basic imports
import numpy as np
import pandas as pd
import seaborn as sns
from   cachai import utilities as util
from   cachai import gadgets
# Matplotlib imports
from   matplotlib import pyplot as plt
from   matplotlib.patches import Arc, Circle, PathPatch
from   matplotlib.path import Path
import matplotlib.colors as mtpl_colors
from   matplotlib.text import Text


class ChordDiagram():
    def __init__(self, corr_matrix, **kwargs):
        """
        Initialize a ChordDiagram visualization.
        """
        # Correlation matrix error handling
        self.corr_matrix = corr_matrix
        self._validate_corr_matrix()
        
        # Initialize additional parameters
        self.__dict__.update(kwargs)
        if isinstance(self.corr_matrix, pd.DataFrame):
            if self.names is None: self.names = self.corr_matrix.columns.tolist()
            self.corr_matrix = self.corr_matrix.to_numpy()
        if self.names is None: self.names = [f'N{i+1}' for i in range(len(self.corr_matrix))]
        if self.colors is None: self.colors = sns.hls_palette(len(self.corr_matrix))
        self.nodes = dict()
        self.order = [i for i in range(len(self.corr_matrix))]
        self.global_indexes = []
        if self.font is None: self.font = {'size':self.fontsize}
        
        # Initialize collection lists
        self.node_patches        = []
        self.node_labels         = []
        self.node_labels_params  = []
        self.chord_patches       = [[] for i in range(len(self.corr_matrix))]
        self.chord_blends        = [[] for i in range(len(self.corr_matrix))]
        self.bezier_curves       = [[] for i in range(len(self.corr_matrix))]
        self.__ports_refs        = []
        self.__highlighted_ports = []
        
        # Generate the diagram
        self.__generate_diagram()
    
    
    # Util methods
    def _validate_corr_matrix(self):
        """Validate that a correlation matrix meets the required specifications:
            - Input is a numpy.ndarray or pandas.DataFrame
            - Matrix is 2-dimensional
            - Matrix is not empty
            - All values are int or float
            - Matrix is symmetric
        """
        temp_corr_matrix = self.corr_matrix
        if not isinstance(temp_corr_matrix, (np.ndarray, pd.DataFrame)):
            raise TypeError('Your correlation matrix must be a numpy.ndarray or pandas.DataFrame')
        # -- This block of code should not be here, but its necessary for the next validations --
        if isinstance(temp_corr_matrix, pd.DataFrame):
            temp_corr_matrix = self.corr_matrix.to_numpy()
        # ---------------------------------------------------------------------------------------
        if temp_corr_matrix.ndim != 2:
            raise ValueError('Your correlation matrix must be a 2-dimensional array')
        if temp_corr_matrix.shape[0] != temp_corr_matrix.shape[1]:
            raise ValueError('Your correlation matrix must be a square matrix.')
        if len(temp_corr_matrix) == 0:
            raise ValueError('Your correlation matrix cannot be empty')
        if not np.issubdtype(temp_corr_matrix.dtype, np.floating):
            raise TypeError('Your correlation matrix must contain float values')
        if not np.allclose(temp_corr_matrix, temp_corr_matrix.T):
            raise ValueError('Your correlation matrix must be symmetric')
        
    def _optimize_nodes(self):
        """Optimize node order using Prim's algorithm."""
        n_nodes = self.corr_matrix.shape[0]
        # We convert the correlations to distances
        # The strongest the correlation, the shorter the distance
        distance_matrix = 1 - np.abs(self.corr_matrix)
        # In order to ignore the diagonal, we fill it with infinity values
        np.fill_diagonal(distance_matrix, np.inf)
        
        # Prim's algorithm
        visited = set()
        order  = []

        start_node = np.argmin(np.sum(distance_matrix, axis=0))
        visited.add(start_node)
        order.append(start_node)

        while len(visited) < n_nodes:
            # Closest non-visited node to any visited node
            min_dist = np.inf
            next_node = -1
            for node in visited:
                for neighbor in range(n_nodes):
                    if (neighbor not in visited) and (distance_matrix[node,neighbor] < min_dist):
                        min_dist = distance_matrix[node, neighbor]
                        next_node = neighbor
            if next_node == -1:
                break  # Just in case somehow we have disconnected nodes
            visited.add(next_node)
            order.append(next_node)

        # Apply new order
        self.order = order
        self.__order_nodes()
    
    def _radius_rule(self, dist):
        """Rule to set the radius of a single chord"""
        if dist <= self.min_dist:
            return self.max_rho_radius
        else:
            return self.max_rho_radius * (1 - (dist - self.min_dist) / (np.pi - self.min_dist))
    
    def _scale_rho(self, rho):
        """Scale rho (link thickness)"""
        if self.scale == 'linear':
            rho_lin = np.abs(rho) * self.max_rho
            return np.clip(rho_lin, 0, 1) # Clip to avoid numerical issues
        elif self.scale == 'log':
            rho_log = (1 - np.log10(10 - 9*np.abs(rho))) * self.max_rho
            return np.clip(rho_log, 0, 1) # Clip to avoid numerical issues
        else:
            raise ValueError(f'Unknown scale type {self.scale}')
    
    # Main generation methods
    def __generate_diagram(self):
        """Generate the complete chord diagram"""
        
        for i,color in enumerate(self.colors):
            if isinstance(color,str): self.colors[i] = mtpl_colors.to_rgb(color)
            
        if self.filter == True: self.__filter_nodes()
        
        if len(self.corr_matrix) == 0:
            raise ValueError(f'No nodes remaining after threshold filtering: '
                f'all correlations were below the threshold = {self.threshold}.')
        else:
            if self.optimize == True: self._optimize_nodes()
            self.__generate_nodes()
            self.__generate_chords()

            # Add patches to axes
            for node_patch, node_label in zip(self.node_patches, self.node_labels_params):
                self.ax.add_patch(node_patch)
                label = gadgets.PolarText(self.position,
                                          node_label['r'],
                                          node_label['theta'],
                                          text=node_label['label'],
                                          pad=self.node_labelpad,
                                          rotation=node_label['rot'],
                                          ha='center', va='center',
                                          clip_on=True,
                                          rasterized=self.rasterized)
                label.set_font(self.font)
                self.ax.add_artist(label)
                self.node_labels.append(label)
            flat_chord_patches = [p for plist in self.chord_patches for p in plist]
            flat_bezier_curves = [c for clist in self.bezier_curves for c in clist]
            for k,(chord_patch,bezier_curve) in enumerate(zip(flat_chord_patches,flat_bezier_curves)):
                self.ax.add_patch(chord_patch)
                if self.blend:
                    self.__add_chord_blend(chord_patch,bezier_curve,self.global_indexes[k])
            
            self.__adjust_ax()
            self.__generate_legend()
            self.__generate_port_refs()
                
    # Components generation methods
    def __generate_nodes(self):
        """Generate nodes"""
        # Initial variables
        # Minus 1 from each diagonal of A to A
        relevance      = np.sum(np.abs(self.corr_matrix),axis=1) - 1
        relevance_norm = relevance / np.sum(relevance)
        start_angles   = np.cumsum([0] + list(2*np.pi*relevance_norm[:-1]))
        gap_angle      = (2*np.pi/len(self.corr_matrix))*self.node_gap

        # Base patch
        self.ax.add_patch(Circle(self.position,self.radius,
                                 lw=0,
                                 zorder=2,
                                 fc='w',
                                 ec='none',
                                 rasterized=self.rasterized))

        lw = 2*self.node_linewidth

        for node in range(len(self.corr_matrix)):
            node_data = dict()
            theta_i   = start_angles[node]
            theta_f   = theta_i + 2*np.pi*relevance_norm[node]
            # -- Gap correction -----
            theta_i   = theta_i + np.min([gap_angle,theta_f])
            # -----------------------
            theta_m   = (theta_i + theta_f)/2
            theta_arc = util.angdist(theta_i,theta_f)
            node_data['theta_i']   = theta_i
            node_data['theta_f']   = theta_f
            node_data['theta_m']   = theta_m
            node_data['theta_arc'] = theta_arc

            rhos       = dict() # Correlations
            ports      = dict() # Ports of the node
            states     = dict() # Ports states (1 or -1)
            corr       = np.insert(self.corr_matrix[node],node,1)
            real_corr  = corr.copy()
            # Control of the allowed ports using the correlation factor
            # 1 = Allowed
            # -1 = Forbidden
            node_ports_state = [1 for p in range(len(corr))]
            for p,r in enumerate(corr):
                if np.abs(r) < self.threshold:
                    node_ports_state[p] = -1
                    real_corr[p]        = 0
            if not self.show_diag:
                node_ports_state[node]   = -1
                real_corr[node]          = 0
                node_ports_state[node+1] = -1
                real_corr[node+1]        = 0
            if np.sum(real_corr) == 0: corr_norm = real_corr
            else: corr_norm = np.abs(real_corr)/np.sum(np.abs(real_corr))

            for j,(rho,port_size,port_state) in enumerate(zip(corr,corr_norm,node_ports_state)):
                if   j == node     : port_id = node
                elif j == (node+1) : port_id = f'{node}*'
                else:
                    if   j < node: port_id = j
                    elif j > node: port_id = j-1
                port_i = theta_i + theta_arc*np.sum(corr_norm[:j])
                port_f = port_i + theta_arc*port_size
                if port_state < 0:
                    port_i = 0
                    port_f = 0
                rhos[port_id]   = rho
                ports[port_id]  = {'i':port_i,'f':port_f}
                states[port_id] = port_state

            node_data['rhos']        = rhos
            node_data['ports']       = ports
            node_data['ports_state'] = states
            self.nodes[node]         = node_data

        # Node
        for n in self.nodes:
            node = self.nodes[n]

            # Patch
            self.node_patches.append(
                Arc(self.position,
                width=2*self.radius, 
                height=2*self.radius,
                theta1=np.rad2deg(node['theta_i']), 
                theta2=np.rad2deg(node['theta_f']),
                lw=lw,zorder=1, 
                rasterized=self.rasterized,
                color=self.colors[n])
            )

            # Label
            params = dict()
            params['label'] = self.names[n]
            params['r']     = self.radius
            params['theta'] = node['theta_m']
            params['x']     = params['r'] * np.cos(params['theta']) + self.position[0]
            params['y']     = params['r'] * np.sin(params['theta']) + self.position[1]
            params['rot']   = np.rad2deg(node['theta_m'] - np.sign(params['y']-self.position[1])*np.pi/2)%360
            self.node_labels_params.append(params)
        
    def __generate_chords(self):
        """Generate chords"""
        for n in self.nodes:
            node = self.nodes[n]
            chord_color = self.colors[n]
            chord_edge  = util.mod_color(self.colors[n],light=0.5)
            if self.blend:
                chord_color = 'none'
                chord_edge = '#3D3D3D'

            # Links
            if self.show_diag:
                points,codes,curve = self.__compute_bezier_curves(
                                         (node['ports'][n]['i'],node['ports'][n]['f']),
                                         (node['ports'][f'{n}*']['i'],node['ports'][f'{n}*']['f']),
                                         self._scale_rho(1)
                                     )

                self.chord_patches[n].append(
                    PathPatch(Path(points, codes),
                              facecolor=chord_color,
                              edgecolor=chord_edge,
                              alpha=self.chord_alpha,
                              hatch=self.positive_hatch,
                              lw=self.chord_linewidth,
                              rasterized=self.rasterized,
                              zorder=4)
                )
                curve['c1'] = self.colors[n]
                curve['c2'] = self.colors[n]
                self.bezier_curves[n].append(curve)
                self.global_indexes.append(n)

            for m in self.nodes:
                if m > n and node['ports_state'][m] > 0:
                    try:
                        target   = self.nodes[m]
                        this_rho = node['rhos'][m]
                        vis_rho  = self._scale_rho(this_rho)
                        hatch    = self.positive_hatch
                        if this_rho < 0: hatch = self.negative_hatch

                        points,codes,curve = self.__compute_bezier_curves(
                                         (node['ports'][m]['i'],node['ports'][m]['f']),
                                         (target['ports'][n]['i'],target['ports'][n]['f']),
                                         vis_rho
                                     )

                        self.chord_patches[n].append(
                            PathPatch(Path(points, codes),
                                      facecolor=chord_color,
                                      edgecolor=chord_edge,
                                      alpha=self.chord_alpha,
                                      hatch=hatch,
                                      lw=self.chord_linewidth,
                                      rasterized=self.rasterized,
                                      zorder=4)
                        )
                        curve['c1'] = self.colors[n]
                        curve['c2'] = self.colors[m]
                        self.bezier_curves[n].append(curve)
                        self.global_indexes.append(n)
                        
                    except Exception as e:
                        print(util.textco(rf'ChordError: Problem creating chord from {self.names[n]} to {self.names[m]}.',
                                          c='red'))
                        print(util.textco(f'            details: {e}',
                                          c='red'))
    
    def __generate_legend(self):
        """Add dummie labels to show in the legend"""
        if self.legend is True:
            if self.positive_label is None: self.positive_label = 'Positive\ncorrelation'
            if self.negative_label is None: self.negative_label = 'Negative\ncorrelation'
        # Dummies
        if self.positive_label is not None:
            dummy = self.ax.scatter(*self.position,marker='s',s=200,
                                    c='lightgray',ec='k',hatch=self.positive_hatch,
                                    label=self.positive_label,zorder=0,rasterized=True)
            #dummy.set_visible(False)
        if self.negative_label is not None:
            dummy = self.ax.scatter(*self.position,marker='s',s=200,
                                    c='lightgray',ec='k',hatch=self.negative_hatch,
                                    label=self.negative_label,zorder=0,rasterized=True)
            #dummy.set_visible(False)
    
    def __generate_port_refs(self):
        for n in self.nodes:
            self.__ports_refs.append(self.__get_node_ports_references(n))

    # Helper methods
    def __filter_nodes(self):
        """Remove nodes with no correlation (0 chords)"""
        mask = np.all((np.abs(self.corr_matrix) < self.threshold)\
                      | (np.eye(self.corr_matrix.shape[0], dtype=bool)), axis=1)
        indexes = np.where(~mask)[0]
        
        self.corr_matrix = self.corr_matrix[indexes][:, indexes]
        self.names       = [self.names[i] for i in indexes]
        self.colors      = [self.colors[i] for i in indexes]
        
    def __order_nodes(self):
        """Order nodes (matrix), names and colors"""
        self.corr_matrix = self.corr_matrix[np.ix_(self.order, self.order)]
        self.names       = [self.names[i] for i in self.order]
        self.colors      = [self.colors[i] for i in self.order]
    
    def __compute_bezier_curves(self,alpha,beta,rho):
        """Compute bezier curves to modelate a chord"""
        # Polar
        alpha_i, alpha_f = alpha
        alpha_m = np.mean([alpha_f,alpha_i])
        alphas = util.angspace(alpha_i,alpha_f)
        if len(alphas) == 0: alphas = np.array([alpha_i,alpha_f]) # Case: angdist too short

        beta_i, beta_f = beta
        beta_m = np.mean([beta_f,beta_i])
        betas = util.angspace(beta_i,beta_f)
        if len(betas) == 0: betas = np.array([beta_i,beta_f]) # Case: angdist too short

        dist = util.angdist(alpha_m, beta_m)
        r_rho = self._radius_rule(dist) * self.radius
        dist_inex = np.min([util.angdist(alpha_i, beta_f), util.angdist(alpha_f, beta_i)])

        # Convex case
        if util.angdist(alpha_i, beta_f) < util.angdist(alpha_f, beta_i):
            theta_rho = beta_f + dist_inex / 2
            r_AB = r_rho
            r_BA = r_rho + rho * self.radius
        # Concave case
        elif util.angdist(alpha_i, beta_f) >= util.angdist(alpha_f, beta_i):
            theta_rho = alpha_f + dist_inex / 2
            r_AB = r_rho + rho * self.radius
            r_BA = r_rho

        # Cartesian
        points_A = np.column_stack([np.cos(alphas) * self.radius, 
                                   np.sin(alphas) * self.radius])
        points_B = np.column_stack([np.cos(betas) * self.radius, 
                                   np.sin(betas) * self.radius])

        # A to B
        point_AB = [np.array([r_AB * np.cos(theta_rho), 
                             r_AB * np.sin(theta_rho)])]
        control_AB = [2 * point_AB[0] - (points_A[-1] + points_B[0]) / 2]

        # B to A
        point_BA = [np.array([r_BA * np.cos(theta_rho), 
                             r_BA * np.sin(theta_rho)])]
        control_BA = [2 * point_BA[0] - (points_A[0] + points_B[-1]) / 2]

        # Bezier curve in the middle
        mid_bezier = dict()
        r_mid = (r_AB + r_BA) / 2
        point_mid = [np.array([r_mid * np.cos(theta_rho), 
                              r_mid * np.sin(theta_rho)])]
        control_mid = [2 * point_mid[0] - (points_A[-1] + points_B[0]) / 2]
        mid_bezier['P0'] = points_A[-1] + self.position
        mid_bezier['P1'] = control_mid[0] + self.position
        mid_bezier['P2'] = points_B[0] + self.position

        # Points
        points = np.vstack((points_A, control_AB, points_B, control_BA, points_A[0])) \
                 + self.position

        # Codes
        codes = [Path.MOVETO] + \
                [Path.LINETO] * (len(points_A) - 1) + \
                [Path.CURVE3] * 2 + \
                [Path.LINETO] * (len(points_B) - 1) + \
                [Path.CURVE3] * 2

        return points,codes,mid_bezier
    
    def __add_chord_blend(self,patch,curve,n):
        """Add color mapped patches using the initial and final colors"""
        # Pach vertices
        vertices = patch.get_path().vertices
        xmin, ymin = np.min(vertices, axis=0)
        xmax, ymax = np.max(vertices, axis=0)

        # Bézier curve
        P0 = curve['P0']
        P1 = curve['P1']
        P2 = curve['P2']
        bezier = util.get_bezier_curve(P0,P1,P2,n=self.bezier_n)
        bezier_equidistant = util.equidistant(bezier)

        # Color map
        norm        = mtpl_colors.Normalize(vmin=-1, vmax=1)
        c1          = curve['c1'] # Color 1
        c2          = curve['c2'] # Color 2
        chord_cmap  = sns.blend_palette([c1,c1,c2,c2],as_cmap=True)
        cmap_matrix = util.map_from_curve(bezier_equidistant,xlims=(xmin,xmax),ylims=(ymin,ymax),
                                     resolution=self.blend_resolution)
        self.chord_blends[n].append(
            util.colormapped_patch(
                patch,
                cmap_matrix,
                ax=self.ax,
                colormap=chord_cmap,
                zorder=2,
                alpha=self.chord_alpha,
                rasterized=self.rasterized)
        )
    
    def __adjust_ax(self):
        """Adjust scale, limits, and visibility of the axis"""
        adjust_x = self.ax.get_autoscalex_on()
        adjust_y = self.ax.get_autoscaley_on()
        if adjust_x:
            self.ax.set_xlim(self.position[0] - self.radius*1.5,self.position[0] + self.radius*1.5)
        if adjust_y:
            self.ax.set_ylim(self.position[1] - self.radius*1.5,self.position[1] + self.radius*1.5)
        if adjust_x and adjust_y: self.ax.set_aspect('equal')
        if self.show_axis == False: self.ax.axis('off')
    
    def __get_node_ports(self,n):
        """Return the occupied ports of the n-th node"""
        this_items = list(self.nodes[n]['ports_state'].items())
        this_items.pop(n+1)
        return [p for p, s in this_items if s > 0 and p > n]

    def __get_node_ports_references(self,n):
        """
        Return the reference of the chords of the n-th node as (n,c), where:

        - n: index of the n-th node in the resulting diagram
        - c: index of the c-th chord in the n-th node

        Always anti-clockwise. When show_diag=True, the self-referencing chord is (n,0).
        """
        node       = self.nodes[n]
        this_ports = self.__get_node_ports(n)
        refs       = []
        for port in node['ports_state'].keys():
            if '*' not in str(port):
                if node['ports_state'][port] > 0 and port > n:
                    refs.append((n,this_ports.index(port)))
                elif node['ports_state'][port] > 0 and port < n:
                    target_ports = self.__get_node_ports(port)
                    refs.append((port,target_ports.index(n)))
        if self.show_diag:
            diag_ref_position = None
            refs_modified = []
            for i, (x, y) in enumerate(refs):
                modified = (x, y + 1)
                refs_modified.append(modified)
                if diag_ref_position is None and x == n: diag_ref_position = i   
            if diag_ref_position is None: diag_ref_position = len(refs_modified)
            refs_modified.insert(diag_ref_position, (n, 0))
            refs = refs_modified
        return refs

    def __update_highlights(self):
        for n in self.nodes:
            for c in range(len(self.chord_patches[n])):
                if (n,c) not in self.__highlighted_ports:
                    self.chord_patches[n][c].set_alpha(self.off_alpha)
                    if self.blend == True: self.chord_blends[n][c].set_alpha(self.off_alpha)

    # Customization methods
    def highlight_node(self,node:int,chords:list=None,alpha:float=None):
        """
        Targeted highlighting of the n-th node
        You can also select the chords that you want to highlight using chords = [0,1,...]
        """
        if node >= len(self.nodes):
            raise IndexError('Node is out of range. '
                f'This Chord Diagram has only {len(self.nodes)} nodes.')
        if node < 0 :
            raise ValueError('The input node must be positive or zero.')

        if chords is None: chords = [c for c in range(len(self.__ports_refs[node]))]
        for chord in chords:
            self.highlight_chord(node,chord,alpha)

    def highlight_chord(self,node:int,chord:int,alpha:float=None):
        """Targeted highlighting of the c-th chord in the n-th node"""
        if node >= len(self.nodes):
            raise IndexError('Node is out of range. '
                f'This Chord Diagram has only {len(self.nodes)} nodes.')
        if node < 0 or chord < 0:
            raise ValueError('The input node and chord must be positive or zero.')

        if alpha is None: alpha = self.chord_alpha
        if alpha <= self.off_alpha: alpha = 0.8

        self.__update_highlights()

        try:
            n,c = self.__ports_refs[node][chord]
            self.chord_patches[n][c].set_alpha(alpha)
            if self.blend == True: self.chord_blends[n][c].set_alpha(alpha)
            if (n,c) not in self.__highlighted_ports: self.__highlighted_ports.append((n,c))
        except IndexError:
            raise IndexError(f'Chord {chord} is out of range. '
                    f'Node {node} has only {len(self.__ports_refs[node])} chords.')

    def set_chord_alpha(self,alpha):
        for n in self.nodes:
            for cp in self.chord_patches[n]: cp.set_alpha(alpha)
            if self.blend == True:
                for cb in self.chord_blends[n]: cb.set_alpha(alpha)

    # Special methods 
    def __str__(self):
        string = ''
        for n in self.nodes:
            string += f'node {n} "{self.names[n]}"\n' + '-'*50
            for key in self.nodes[n]:
                if key == 'ports':
                    string += f'\n{key:<10} :'
                    for p in self.nodes[n][key]:
                        string += f'\n\t\t{p:<10} : {self.nodes[n][key][p]}'
                else:
                    string += f'\n{key:<10} : {self.nodes[n][key]}'
            string += '\n\n\n'
        return string